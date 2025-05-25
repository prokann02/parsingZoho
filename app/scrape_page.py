from app.extract_structured_items import extract_structured_items
from app.get_links_from_page import get_links_from_page


def scrape_page(url, browser, depth=1, visited=None):
    if visited is None:
        visited = set()
    scraped_data = []

    page = browser.new_page()
    try:
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle", timeout=10000)
        print(f"Scraping: {url}")

        visited.add(url)

        items = extract_structured_items(page)

        if items:
            scraped_data.append({
                "url": url,
                "items": items
            })
        else:
            print(f"[i] Skipping content for hub page: {url}")

        # Continue go through links, if depth > 1
        if depth > 1:
            internal_links = get_links_from_page(page, url)
            for link in internal_links:
                if link not in visited:
                    # if link == 'https://help.zoho.com/portal/en/kb/crm/getting-started/articles/understand-crm-account':
                    data = scrape_page(url=link, depth=depth - 1, visited=visited, browser=browser)
                    if data:
                        scraped_data.extend(data)

    except Exception as e:
        print(f"[!] Failed to scrape {url}: {e}")
    finally:
        page.close()
    return scraped_data
