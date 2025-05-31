from bs4 import Tag, BeautifulSoup

from .process_top_level import process_top_level


async def extract_structured_items(page):
    try:
        box = page.locator('.ArticleDetailLeftContainer__box')
        if await box.count() == 0:
            print("[i] No elements found for selector")
            return []

        html = await box.inner_html()
        soup = BeautifulSoup(html, 'html.parser')
        items = []

        # Go only through the upper-level children of the container
        for element in soup.contents:
            if isinstance(element, Tag):
                await process_top_level(tag=element, items=items)

        category_items = []
        breadcrumbs = page.locator("ul.BreadCrumbs__breadcrumbList li")
        count = await breadcrumbs.count()
        for i in range(count):
            item = breadcrumbs.nth(i)
            text = await item.inner_text()
            category_items.append(text.strip())

        category_path = " > ".join(category_items) if category_items else None
        print("category_path", category_path)
        return items, category_path

    except Exception as e:
        print(f"[!] Error extracting structured content: {e}")
        return []
