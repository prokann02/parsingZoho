import json

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from playwright.async_api import async_playwright

from app.scrape_page import scrape_page
from paths import TEMPLATES_FORM_HTML, TEMPLATES, TEMPLATES_SELECT_LINKS_HTML

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES)


# For css
# app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse(TEMPLATES_FORM_HTML, {"request": request})


@app.post("/start", response_class=HTMLResponse)
async def start_scrape(request: Request, url: str = Form(...), depth: int = Form(...)):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        results = await scrape_page(url, depth=depth, browser=browser)
        await browser.close()

    with open("scraped_zoho2.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return templates.TemplateResponse(TEMPLATES_SELECT_LINKS_HTML, {"request": request, "results": results})

# import json
#
# from playwright.sync_api import sync_playwright
#
# from zoho_scraper.scraper.app.scrape_page import scrape_page
#
#
# def main():
#     start_url = "https://help.zoho.com/portal/en/kb/crm/"  # TODO: change
#     depth = 2  # TODO: change
#
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         results = scrape_page(start_url, depth=depth, browser=browser)
#         browser.close()
#
#     with open("scraped_zoho2.json", "w", encoding="utf-8") as f:  # TODO: change
#         json.dump(results, f, ensure_ascii=False, indent=2)
#
#
# if __name__ == "__main__":
#     main()
