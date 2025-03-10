import json

from transformers import pipeline


def transformers_get_sentiment_scores(input_path):
    sentiment_pipeline = pipeline("sentiment-analysis")

    with open(input_path, "r") as file:
        articles = json.load(file)
    results = sentiment_pipeline([article["content"] for article in articles], truncation=True)
    return map(
        lambda result: round(result["score"], 2) if result["label"] == "POSITIVE" else -round(result["score"], 2),
        results)
