from bs4 import Tag

from .chunk_text import chunk_text
from .clean_text import clean_text, looks_like_nav_page


async def process_top_level(tag: Tag, items: list):
    allowed_containers = ['div', 'p', 'section', 'article']

    if not isinstance(tag, Tag):
        return
    if tag.name not in allowed_containers:
        return

    text = await clean_text(tag)
    if not text.strip():  # or await looks_like_nav_page(text):
        return

    for chunk in await chunk_text(text):
        items.append({
            # "tag": tag.name,
            # "class": tag.get('class', []),
            "text": chunk
        })
