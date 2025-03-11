import requests
from bs4 import BeautifulSoup

URL = "https://www.cbc.ca/search_api/v1/search"


def _make_request(url, params=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response


def requests_scrape_cbc_news(query="Vancouver", count=10):
    params = {
        "q": query,
        "section": "news",
        "sortOrder": "relevance",
        "media": "all",
        "boost-cbc-keywords": 7,
        "boost-cbc-keywordscollections": 7,
        "boost-cbc-keywordslocation": 4,
        "boost-cbc-keywordsorganization": 3,
        "boost-cbc-keywordsperson": 5,
        "fields": "feed",
        "page": 1
    }
    results = []
    scraped_urls = set()
    while len(results) < count:
        response = _make_request(URL, params=params).json()
        for item in response:
            if item["category0"] == "news" and item["url"] not in scraped_urls:
                article = get_article_content(url="https:" + item["url"])
                results.append(article)
                scraped_urls.add(item["url"])
                print(f"{len(results)}. {article['title']}")
        params["page"] += 1
    return results


def get_article_content(url):
    response = _make_request(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return dict(
        title=soup.select_one("h1.detailHeadline").get_text(strip=True),
        content=soup.select_one("div.story").get_text(strip=True),
        date=soup.select_one("time").get("datetime"),
        url=url
    )



