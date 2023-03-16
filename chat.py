import openai
import re

from dataclasses import dataclass
from search import *

openai.api_key = os.getenv("OPENAI_API_KEY")

SEARCH_REGEX = r"\[SEARCH REQUEST: (.*)\]"
FORCE_PROMPT = " Remember that you can use [SEARCH REQUEST: xxx] to indicate you need a search result for the keyword xxx."
SEARCH_RESULT = """The following is the search result: {}
Please answer the previous question with this information and do not issue another search request."""

INITIAL_USER_PROMPT = """From now on, when you need some information you don't know,
indicate that you need a google search result by saying [SEARCH REQUEST: xxx] and nothing else,
where xxx is the term you want to search. You will always issue a search request whenever you need information that you don't know.
Do not fake any result about things you don't know, especially about current situation and events."""
INITIAL_ASSISTANT_RESP = """Understood. Whenever I need additional information that I don't have knowledge of,
I will indicate that by using the format [SEARCH REQUEST: xxx] where xxx is the keyword, and say nothing else."""

# message status
SHOW_UNCHECKED = 0
SHOW_CHECKED = 1
HIDE = 2

@dataclass
class Line:
    msg: str
    status: int

    def _update_status(self):
        if "The following is the search result:" in self.msg['content'] \
                or len(re.findall(SEARCH_REGEX, self.msg['content'])) > 0:
            self.status = HIDE
        else:
            self.status = SHOW_CHECKED

    def get_msg(self):
        if self.status == SHOW_UNCHECKED:
            self._update_status()
        return self.msg

    def pprint(self):
        print("{}\t{}: {}\n".format(self.status, self.msg['role'], self.msg['content']))
        

def detect_failure(resp):
    return "as an ai language model" in resp.lower()

class Chat:
    lines = [
        Line({"role": "user", "content": INITIAL_USER_PROMPT}, SHOW_CHECKED),
        Line({"role": "assistant", "content": INITIAL_ASSISTANT_RESP}, SHOW_CHECKED)
    ]

    def _messages(self):
        return [l.get_msg() for l in self.lines if l.status != HIDE]

    def _append_line(self, role, content):
        self.lines.append(Line({"role": role, "content": content}, SHOW_UNCHECKED))

    def _talk(self, prompt):
        self._append_line("user", prompt)
        rtn = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._messages()
        )
        msg = dict(rtn["choices"][0]["message"])
        role, content = msg["role"], msg["content"]
        self._append_line(role, content)
        return content

    def talk(self, prompt, force=False):
        resp = self._talk(prompt)
        requests = re.findall(SEARCH_REGEX, resp)
        if not requests or requests[0] == "xxx":
            if detect_failure(resp):
                if not force:
                    print("----- debug: force -----")
                    return self.talk(prompt + FORCE_PROMPT, force=True)
            return resp
        if len(requests) > 1:
            raise NotImplemented("multiple search requests")
        print("----- debug: search request: {} -----".format(requests[0]))
        search_result = get_nl(search(requests[0]))
        # print("----- debug: search result -----\n{}\n----- debug: end search result -----".format(search_result))
        return self._talk(SEARCH_RESULT.format(search_result))

c = Chat()
prompt = input("User: ")
while prompt != "exit":
    if not prompt:
        prompt = input("User: ")
        continue
    if prompt.startswith('!'):
        eval(prompt[1:])  # !!!!DANGEROUS!!!!
        prompt = input("User: ")
        continue
    resp = c.talk(prompt)
    print("Assistant:", resp)
    prompt = input("User: ")
