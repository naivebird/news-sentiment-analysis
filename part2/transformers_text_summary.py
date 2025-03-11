import json
from transformers import pipeline


def transformers_summarize_text(input_path):
    summarizer_pipeline = pipeline('summarization')

    with open(input_path, "r") as file:
        articles = json.load(file)

    print("Summarizing articles...")

    return summarizer_pipeline([article["content"] for article in articles], truncation=True)


if __name__ == '__main__':
    results = transformers_summarize_text("./../data/articles.json")
    print(results)