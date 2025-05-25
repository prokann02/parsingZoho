from urllib.parse import urljoin, urlparse


async def get_links_from_page(page, base_url):
    links = await page.locator('a').all()
    internal_links = set()

    for link in links:
        href = await link.get_attribute('href')
        if href and not href.startswith(('mailto:', 'tel:', 'javascript:')):
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                internal_links.add(full_url)

    return list(internal_links)
