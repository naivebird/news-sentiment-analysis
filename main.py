import csv
import json
import time

from part1.playwright_cbc_news import playwright_scrape_cbc_news
from part1.requests_cbc_news import requests_scrape_cbc_news
from part2.transformers_cbc_news import transformers_get_sentiment_scores
from part2.vader_sentiment_cbc_news import vader_get_sentiment_scores

NEWS_PATH = "data/articles.json"
SENTIMENT_SCORES_PATH = "data/sentiment_scores.csv"


def benchmark(func, **kwargs):
    start = time.time()
    result = func(**kwargs)
    end = time.time()
    print(f"{func.__name__}: {end - start:.2f} seconds")
    return result


def benchmark_playwright_vs_requests(article_count):
    benchmark(func=playwright_scrape_cbc_news,
              count=article_count)

    results = benchmark(func=requests_scrape_cbc_news,
                        count=article_count)

    with open(NEWS_PATH, "w") as file:
        json.dump(results, file, indent=4)


def save_sentiment_scores(vader_sentiment_scores, transformers_sentiment_scores):
    with open(SENTIMENT_SCORES_PATH, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "content", "date", "url", "vader sentiment score", "transformers sentiment score"])
        with open(NEWS_PATH, "r") as news_file:
            articles = json.load(news_file)
            for article, vader_score, transformers_score in zip(
                    articles,
                    vader_sentiment_scores,
                    transformers_sentiment_scores
            ):
                writer.writerow(
                    [article["title"],
                     article["content"],
                     article["date"],
                     article["url"],
                     vader_score,
                     transformers_score]
                )
    print(f"Sentiment scores saved to {SENTIMENT_SCORES_PATH}")


def benchmark_vader_vs_transformers():
    vader_sentiment_scores = benchmark(func=vader_get_sentiment_scores,
                                       input_path=NEWS_PATH)

    transformers_sentiment_scores = benchmark(func=transformers_get_sentiment_scores,
                                              input_path=NEWS_PATH)

    save_sentiment_scores(vader_sentiment_scores, transformers_sentiment_scores)


def part1():
    benchmark_playwright_vs_requests(article_count=100)


def part2():
    benchmark_vader_vs_transformers()


if __name__ == '__main__':
    part1()
    # playwright_scrape_cbc_news: 179.28 seconds
    # requests_scrape_cbc_news: 31.87 seconds

    part2()
    # vader_get_sentiment_scores: 1.02 seconds
    # transformers_get_sentiment_scores: 29.16 seconds
