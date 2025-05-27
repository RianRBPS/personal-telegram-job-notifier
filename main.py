import json
import time
import asyncio
from job_sources.craigslist import fetch_jobs
from bot.telegram_sender import send_jobs

SENT_JOBS_FILE = "sent/craigslist.json"

def load_sent_jobs():
    try:
        with open(SENT_JOBS_FILE, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_sent_jobs(sent_ids):
    with open(SENT_JOBS_FILE, "w") as f:
        json.dump(list(sent_ids), f)

def main():
    print("Fetching jobs...")
    sent = load_sent_jobs()
    jobs = fetch_jobs()
    print(f"{len(jobs)} jobs found (filtered by scraper).")

    new_jobs = [job for job in jobs if job["id"] not in sent]
    print(f"{len(new_jobs)} new jobs to send.")

    if new_jobs:
        asyncio.run(send_jobs(new_jobs))
        sent.update([job["id"] for job in new_jobs])
        save_sent_jobs(sent)
        print("Jobs sent and saved.")
    else:
        print("⏸ No new jobs.")

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error during run: {e}")
        time.sleep(60 * 15)  # run every 15 minutes
