from bs4 import Tag


async def looks_like_nav_page(text):
    garbage_keywords = ["skip to", "sign in", "contact us", "terms of service", "sign up"]
    return any(kw in text.lower() for kw in garbage_keywords)


async def clean_text(tag: Tag):
    return tag.get_text(separator='\n', strip=True)
