from playwright._impl._errors import TimeoutError
from playwright.sync_api import sync_playwright

URL = "https://www.cbc.ca/search?q=Vancouver&section=news&sortOrder=relevance&media=all"


def go_to_page(page, url, max_retries=5):
    retry_count = 0
    while True:
        try:
            page.goto(url, timeout=30000)
            break
        except TimeoutError:
            retry_count += 1
            if retry_count >= max_retries:
                raise TimeoutError(f"Failed to load {url} after {max_retries} retries")
            print(f"Retrying to load {url}... Attempt {retry_count}")


def playwright_scrape_cbc_news(count=100):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        go_to_page(page, URL)
        links = set()
        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            articles = page.locator("div.contentListCards a.card[data-cy=type-story]").all()

            if len(articles) >= count:
                for article in articles:
                    link = "https://www.cbc.ca" + article.get_attribute("href")
                    links.add(link)
                    if len(links) >= count:
                        break
                break

            load_more_button = page.locator("div.contentList button")
            load_more_button.click()

        results = []
        for link in links:
            go_to_page(page, link)
            article = dict(
                title=page.locator("h1.detailHeadline").inner_text(),
                content=page.locator("div.story").inner_text(),
                date=page.locator("time").get_attribute("datetime"),
                url=link,
            )
            results.append(article)

            print(f"{len(results)}. {article['title']}")

        browser.close()

        return results
