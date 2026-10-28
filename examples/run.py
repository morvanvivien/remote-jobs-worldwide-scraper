"""Minimal example: run the remote-jobs-worldwide-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "keywords": "backend engineer",
    "region": "anywhere",
    "sources": [
        "remoteok",
        "remotive",
        "weworkremotely",
        "jobicy",
        "workingnomads",
        "hackernews",
        "wellfound",
        "getonbrd",
    ],
    "publishedWithinDays": 7,
    "maxItems": 100,
    "includeDescriptions": False,
}

run = client.actor("bibian/remote-jobs-worldwide-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    salary_min = item.get("salaryMin")
    salary_max = item.get("salaryMax")
    if salary_min or salary_max:
        pay = f"{salary_min or '-'}-{salary_max or '-'} {item.get('salaryCurrency') or ''}/{item.get('salaryPeriod') or '?'}"
    else:
        pay = "n/a"
    print(f"{item['title']} | {item.get('companyName') or 'confidential'} | {item.get('locationLabel') or 'remote'} | {item.get('source')} | {pay}")
print(f"{count} results")
