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
I used 2 libraries, Playwright and (Requests + BeautifulSoup) to separately scrape 100 news articles about Vancouver from the CBC news and benchmark their performance.
Run the scrapers:
```python
python main.py
```
After the program finishes running, you can find 100 scraped news articles in `data/articles.json`
Bechmark results:
```
playwright_scrape_cbc_news: 179.28 seconds
requests_scrape_cbc_news: 31.87 seconds
```
### Observations
Playwright is significantly more resource-intensive than Requests as you have to download its browswers when setting it up and spin up a browser (in headful mode) when running it.
Requests, on the other hand, is substantially faster, much more lightweight and resource efficient.
But there's catch, Requests is only good for interacting with static web pages or APIs, and handling HTTP communications without the need for browser automation. 
Playwright shines when you have to interact with web pages (e.g., click buttons, fill forms) and scrape dynamic content rendered by JavaScript as you can't achieve this with Requests.
To sum up, you should use Requests + BeautifulSoup when applicable to minimize the overhead and speed up your development unless Playwright is requried.
For this assignment, using Requests is more than enough.
