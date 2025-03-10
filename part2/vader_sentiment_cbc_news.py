import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def vader_get_sentiment_scores(input_path):
    sentiment = SentimentIntensityAnalyzer()

    with open(input_path, "r") as file:
        articles = json.load(file)
    return [round(sentiment.polarity_scores(article["content"])["compound"], 2) for article in articles]
