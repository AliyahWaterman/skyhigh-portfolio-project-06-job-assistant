def deduplicate_listings(listings):
    """
    Remove duplicate job listings that appear more than once
    (e.g. same job pulled from two different sources).
    Two listings are considered the same if they share the same URL,
    or the same title + company combination.
    """
    seen_urls = set()
    seen_title_company = set()
    unique_listings = []

    for job in listings:
        url = job.get("url")
        title_company = (job.get("title"), job.get("company"))

        if url in seen_urls or title_company in seen_title_company:
            continue  # skip — we've already got this one

        seen_urls.add(url)
        seen_title_company.add(title_company)
        unique_listings.append(job)

    return unique_listings
