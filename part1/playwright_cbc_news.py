from playwright.sync_api import sync_playwright

URL = "https://www.cbc.ca/search?q=Vancouver&section=news&sortOrder=relevance&media=all"


def scrape_cbc_news(count=100):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
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
        n = 0
        for link in links:
            page.goto(link)
            article = dict(
                title=page.locator("h1.detailHeadline").inner_text(),
                link=link,
                date=page.locator("time").get_attribute("datetime"),
                content=page.locator("div.story").inner_text(),
            )
            results.append(article)
            n += 1

            print(f"{n}. {article['title']}")

        browser.close()

        return results


if __name__ == "__main__":
    news_results = scrape_cbc_news(count=10)
