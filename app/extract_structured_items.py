from bs4 import Tag, BeautifulSoup

from .process_top_level import process_top_level


async def extract_structured_items(page):
    try:
        box = await page.locator('.ArticleDetailLeftContainer__box')
        if await box.count() == 0:
            return []

        html = await box.inner_html()
        soup = BeautifulSoup(html, 'html.parser')
        items = []

        # Go only through the upper-level children of the container
        for element in soup.contents:
            if isinstance(element, Tag):
                await process_top_level(tag=element, items=items)

        return items

    except Exception as e:
        print(f"[!] Error extracting structured content: {e}")
        return []
