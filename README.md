# Peripheral
> ... for chatGPT to make it more powerful

#### Showcase

```
# Before:
User: How was the score of today's (Mar 15, 2023) Real Madrid game?
Assistant: I'm sorry, but as an AI language model with a knowledge cutoff in September 2021, I am unable to provide you with the score of the Real Madrid game on March 15, 2023. To find the most recent scores and updates, I recommend checking sports websites, news outlets, or the official Real Madrid website.

# After:
User: How was the score of today's (Mar 15, 2023) Real Madrid game?
Assistant: Based on the search results, Real Madrid defeated Liverpool 1-0 in the UEFA Champions League match played on March 15, 2023. Karim Benzema scored the winning goal for Real Madrid in the match, which was held at the Estadio Santiago Bernabeu stadium in Madrid, Spain.
```

```
# Before:
User: What is the market cap of Apple vs Google as of today?
Assistant: As an AI language model, I don't have real-time data access, and my knowledge was last updated in September 2021. To find the most recent market capitalization for Apple and Google (Alphabet), I recommend checking financial news websites or using financial tools like Google Finance or Yahoo Finance for the latest information. Keep in mind that market capitalization values can change frequently due to stock price fluctuations.

# After:
User: What is the market cap of Apple vs Google as of today?
Assistant: Based on the search result, as of March 15, 2023, Google's parent company, Alphabet, has a market cap of $2.144 trillion, while Apple's market cap is $2.407 trillion, making Apple the company with the larger market cap.
```

#### TODO:
- [Toolformer](https://arxiv.org/abs/2302.04761)
- The current behavior (especially the gpt-3.5-turbo model that's available for API) is not stable (check the run_log folder for more realistic experience), might be improved by:
    - Use better prompt engineering
    - [Fine tune the model](https://platform.openai.com/docs/guides/fine-tuning)