from bs4 import Tag

from app.chunk_text import chunk_text
from app.clean_text import clean_text


def process_top_level(tag: Tag, items: list):
    allowed_containers = ['div', 'p', 'section', 'article']

    if not isinstance(tag, Tag):
        return
    if tag.name not in allowed_containers:
        return

    text = clean_text(tag)
    if not text.strip():
        return

    for chunk in chunk_text(text):
        items.append({
            # "tag": tag.name,
            # "class": tag.get('class', []),
            "text": chunk
        })
