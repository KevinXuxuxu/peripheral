import os
import requests as rq

API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

URL = 'https://customsearch.googleapis.com/customsearch/v1?cx={cx}&q={q}&key={key}'

def search(keyword):
    url = URL.format(cx=CX, key=API_KEY, q=keyword.replace(' ', '%20'))
    rtn = rq.get(url, headers={'Accept': 'application/json'})
    return rtn.json()

def get_nl(rtn_json):
    return [[item['title'], item['snippet']] for item in rtn_json['items']]
