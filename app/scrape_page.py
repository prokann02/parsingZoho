from .extract_structured_items import extract_structured_items
from .get_links_from_page import get_links_from_page
import json

async def scrape_page(url, browser, depth=1, visited=None):
    if visited is None:
        visited = set()

    if url in visited:
        return {"results": [], "links": []}

    visited.add(url)
    scraped_data = []
    internal_links = []

    page = await browser.new_page()
    try:
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle", timeout=10000)
        print(f"Scraping: {url}")

        items, category = await extract_structured_items(page)
        print(f"[i] Extracted {len(items)} items for {url}")

        if items:
            scraped_data.append({
                "url": url,
                "items": items,
                "category": category,
            })

            # Save parted data to JSON file
            try:
                with open("scraped_zoho.json", "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = []
            existing_data.extend(scraped_data)
            with open("scraped_zoho.json", "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
        else:
            print(f"[i] Skipping content for hub page: {url}")

        if depth >= 1:
            internal_links = await get_links_from_page(page, url)
            internal_links = [link for link in internal_links if link not in visited]
            print(f"[i] Found {len(internal_links)} internal links")

    except Exception as e:
        print(f"[!] Failed to scrape {url}: {e}")
    finally:
        await page.close()

    return {"results": scraped_data, "links": internal_links}