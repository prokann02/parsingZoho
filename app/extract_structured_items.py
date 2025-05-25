from bs4 import Tag, BeautifulSoup

from app.process_top_level import process_top_level


def extract_structured_items(page):
    try:
        box = page.locator('.ArticleDetailLeftContainer__box')
        if box.count() == 0:
            return []

        html = box.inner_html()
        soup = BeautifulSoup(html, 'html.parser')
        items = []

        # Go only through the upper-level children of the container
        for element in soup.contents:
            if isinstance(element, Tag):
                process_top_level(tag=element, items=items)

        return items

    except Exception as e:
        print(f"[!] Error extracting structured content: {e}")
        return []
