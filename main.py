import json
import uuid

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from playwright.async_api import async_playwright

from app.scrape_page import scrape_page
from paths import TEMPLATES_FORM_HTML, TEMPLATES, TEMPLATES_SELECT_LINKS_HTML, TEMPLATES_RESULT_HTML, STATIC

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES)
app.mount("/static", StaticFiles(directory=STATIC), name="static")

scraping_session = {}

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse(TEMPLATES_FORM_HTML, {"request": request})

@app.post("/scrape", response_class=HTMLResponse)
async def start_scrape(request: Request, url: str = Form(...), depth: int = Form(...)):
    if not url or depth < 0:
        return templates.TemplateResponse(
            TEMPLATES_FORM_HTML,
            {"request": request, "url": url, "depth": depth, "error": "Please provide a valid URL and depth"}
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            scrape_data = await scrape_page(url, browser=browser, depth=1)
            results = scrape_data["results"]
            internal_links = scrape_data["links"]
        except Exception as e:
            print(f"[!] Error in scrape_page: {e}")
            results = []
            internal_links = []
        finally:
            await browser.close()

        print(f"[i] Scraped {len(results)} pages, {sum(len(r['items']) for r in results) if results else 0} items")
        for result in results:
            print(f"[i] Page {result['url']} has {len(result['items'])} items")

        # Save results to JSON even if empty
        with open("scraped_zoho2.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        session_id = str(uuid.uuid4())
        scraping_session[session_id] = {
            "original_url": url,
            "max_depth": depth,
            "current_depth": 1,
            "results": results,
            "links": internal_links
        }

        print(f"[i] Depth: {depth}, Links found: {len(internal_links)}, Redirecting to: {'results' if depth == 0 or not internal_links else 'select_links'}")

        # Always redirect to result.html for depth=0 or no links
        if depth == 0 or not internal_links:
            return templates.TemplateResponse(
                TEMPLATES_RESULT_HTML,
                {"request": request, "results": results, "links": internal_links}
            )
        else:
            return templates.TemplateResponse(
                TEMPLATES_SELECT_LINKS_HTML,
                {
                    "request": request,
                    "links": internal_links,
                    "session_id": session_id,
                    "current_depth": 1,
                    "max_depth": depth
                }
            )

@app.post("/continue_scrape", response_class=HTMLResponse)
async def continue_scrape(request: Request, session_id: str = Form(...), selected_links: list = Form(...)):
    if session_id not in scraping_session:
        return templates.TemplateResponse(
            TEMPLATES_FORM_HTML,
            {"request": request, "error": "Session expired or invalid"}
        )

    session_data = scraping_session[session_id]
    max_depth = session_data["max_depth"]
    current_depth = session_data["current_depth"] + 1
    depth = max_depth - current_depth + 1
    results = session_data["results"]
    new_internal_links = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            for link in selected_links:
                if depth > 0:
                    scrape_data = await scrape_page(link, browser=browser, depth=depth)
                    results.extend(scrape_data["results"])
                    new_internal_links.extend(scrape_data["links"])
                    with open("scraped_zoho2.json", "w", encoding="utf-8") as f:
                        json.dump(results, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[!] Error in continue_scrape: {e}")
        finally:
            await browser.close()

    print(
        f"[i] After continuation at depth {current_depth}: {len(results)} pages, {sum(len(r['items']) for r in results) if results else 0} items")
    print(f"[i] Found {len(new_internal_links)} new internal links")

    visited = {r["url"] for r in results}
    new_internal_links = list(dict.fromkeys([link for link in new_internal_links if link not in visited]))

    scraping_session[session_id]["results"] = results
    scraping_session[session_id]["links"] = new_internal_links
    scraping_session[session_id]["current_depth"] = current_depth

    if new_internal_links and depth > 1:
        return templates.TemplateResponse(
            TEMPLATES_SELECT_LINKS_HTML,
            {
                "request": request,
                "links": new_internal_links,
                "session_id": session_id,
                "current_depth": current_depth,
                "max_depth": max_depth
            }
        )
    else:
        del scraping_session[session_id]
        return templates.TemplateResponse(
            TEMPLATES_RESULT_HTML,
            {"request": request, "results": results, "links": new_internal_links}
        )

@app.get("/stop_and_get_results", response_class=HTMLResponse)
async def stop_and_get_results(request: Request, session_id: str):
    if session_id not in scraping_session:
        return templates.TemplateResponse(
            TEMPLATES_FORM_HTML,
            {"request": request, "error": "Session expired or invalid"}
        )

    session_data = scraping_session[session_id]
    results = session_data["results"]
    internal_links = session_data["links"]

    with open("scraped_zoho2.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    del scraping_session[session_id]

    return templates.TemplateResponse(
        TEMPLATES_RESULT_HTML,
        {"request": request, "results": results, "links": internal_links}
    )


@app.get("/download_results", response_class=FileResponse)
async def download_results():
    try:
        with open("scraped_zoho2.json", "r", encoding="utf-8") as f:
            json.load(f)
        return FileResponse(
            path="scraped_zoho2.json",
            filename="scraped_zoho2.json",
            media_type="application/json"
        )
    except (FileNotFoundError, json.JSONDecodeError):
        return templates.TemplateResponse(
            TEMPLATES_RESULT_HTML,
            {"request": Request, "results": [], "links": [], "error": "No results available to download"}
        )
