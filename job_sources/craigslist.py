from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from config.settings import CRAIGSLIST_SEARCH_URL

SEARCH_URL = CRAIGSLIST_SEARCH_URL

def fetch_jobs():
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SEARCH_URL, timeout=60000)
        page.wait_for_selector("div.cl-search-result", timeout=10000)

        job_blocks = page.query_selector_all("div.cl-search-result")

        for job_block in job_blocks:
            try:
                title_tag = job_block.query_selector("a.posting-title span.label")
                url_tag = job_block.query_selector("a.posting-title")
                time_tag = job_block.query_selector("div.meta span[title]")

                title = title_tag.inner_text().strip() if title_tag else "No Title"
                url = url_tag.get_attribute("href") if url_tag else None
                time_str = time_tag.get_attribute("title") if time_tag else "Unknown"
                post_id = url.split("/")[-1].replace(".html", "") if url else None

                # Clean and parse time (e.g., "Tue May 20 2025 08:40:45 GMT-0700 (PDT)" → "Tue May 20 2025 08:40:45")
                try:
                    clean_time = time_str.split(" GMT")[0].strip()
                    parsed_time = datetime.strptime(clean_time, "%a %b %d %Y %H:%M:%S")
                    if parsed_time < datetime.now() - timedelta(hours=3):
                        continue
                except Exception as e:
                    print(f"Skipping job due to time parsing error: {e}")
                    continue

                if post_id and url:
                    jobs.append({
                        "id": post_id,
                        "title": title,
                        "url": url,
                        "time": time_str
                    })

            except Exception as e:
                print(f"Error parsing job block: {e}")
                continue

        browser.close()

    return jobs
