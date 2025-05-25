import json

from playwright.sync_api import sync_playwright

from app.scrape_page import scrape_page


def main():
    start_url = "https://help.zoho.com/portal/en/kb/crm/"  # TODO: change
    depth = 2  # TODO: change

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        results = scrape_page(start_url, depth=depth, browser=browser)
        browser.close()

    with open("scraped_zoho2.json", "w", encoding="utf-8") as f:  # TODO: change
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
