from sources.greenhouse import fetch_greenhouse_listings
from sources.lever import fetch_lever_listings
from sources.normalize import normalize_greenhouse, normalize_lever
from dedupe import deduplicate_listings
from config import GREENHOUSE_COMPANIES, LEVER_COMPANIES


def collect_all_listings():
    all_jobs = []

    for company in GREENHOUSE_COMPANIES:
        raw_jobs = fetch_greenhouse_listings(company)
        for job in raw_jobs:
            all_jobs.append(normalize_greenhouse(job))

    for company in LEVER_COMPANIES:
        raw_jobs = fetch_lever_listings(company)
        for job in raw_jobs:
            all_jobs.append(normalize_lever(job, company))

    return deduplicate_listings(all_jobs)


if __name__ == "__main__":
    listings = collect_all_listings()
    print(f"Found {len(listings)} unique listings.")
    for job in listings[:3]:
        print(job)
