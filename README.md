## Overview

This repository consists of a `main.py` file and 3 sub-directories `part1`, `part2`, which contain the code for the corresponding parts in the assignment and `data` directory where input and output files are saved.
You can run the `main.py` which calls `part1` and `part2` functions sequentially and generates the final output file in: `data/sentiment_scores.csv`
## Install required packages
Navigate to the project directory:
```bash
cd news-sentiment-analysis
```
Setup your virtual environment
```bash
python -m venv env
cd env/Scripts && activate && cd ../../
```
Install poetry
```bash
pip install poetry
```
Install the dependencies
```bash
poetry install
```
Download playwright browsers
```bash
playwright install
```
## Part 1
### Playwright vs (Requests + BeautifulSoup) benchmark
In part 1, I used 2 libraries, Playwright and (Requests + BeautifulSoup) to separately scrape 100 news articles about Vancouver from the CBC news and benchmark their performance.
Run the scrapers:
```python
python main.py
```
After the program finishes running, you can find 100 scraped news articles in `data/articles.json`
Benchmark results:
```
playwright_scrape_cbc_news: 179.28 seconds
requests_scrape_cbc_news: 31.87 seconds
```
### Observations
Playwright is significantly more resource-intensive than Requests as you have to download its browsers when setting it up and spin up a browser (in headful mode) when running it.
Requests, on the other hand, is substantially faster, much more lightweight, and resource efficient.
But there's a catch, Requests is only good for interacting with static web pages or APIs, and handling HTTP communications without the need for browser automation. 
Playwright shines when you have to interact with web pages (e.g., click buttons, fill forms) and scrape dynamic content rendered by JavaScript as you can't achieve this with Requests.
To sum up, you should use Requests + BeautifulSoup when applicable to minimize the overhead and speed up your development unless a browser is required.
For this assignment, because CBC has a public API for searching articles and their article pages are static, 
using Requests + BeautifulSoup is more than enough.

## Part 2
### Sentiment analysis
In this part, I used the `VADER` sentiment analysis tool and the `transformers` library to analyze the sentiment of the scraped news articles.
Transformers was also used to summarize the articles.

Run the sentiment analysis and text summarization:
```python
python main.py
```
After the program finishes running, you can find the sentiment scores and summaries in `data/sentiment_scores.csv`

Benchmark results:
```
vader_get_sentiment_scores: 1.02 seconds
transformers_get_sentiment_scores: 29.16 seconds
transformers_summarize_text: 783.12 seconds
```

### Observations
VADER is a rule-based sentiment analysis tool specifically attuned to sentiments expressed in social media.
It is fast and easy to use, but it has its limitations.
It doesn't understand context, sarcasm, or irony and doesn't work well with long texts. 
It's good for short texts like tweets, but not for long articles. 
Transformers, on the other hand, is a state-of-the-art NLP model that can be fine-tuned for sentiment analysis and text summarization.
It is much more accurate and can understand context, sarcasm, and irony.
But it is computationally expensive and slow, especially when you have to analyze a large number of articles.
For this assignment, Transformers is the better choice for both sentiment analysis and text summarization as
it is more accurate and can handle long articles.

