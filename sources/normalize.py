import re

def strip_html(raw_html):
    """Removes HTML tags so we get plain readable text."""
    if not raw_html:
        return None
    return re.sub(r"<[^>]+>", " ", raw_html).strip()


def normalize_greenhouse(job):
    """Convert one raw Greenhouse job into the common schema."""
    return {
        "title": job.get("title"),
        "company": job.get("company_name"),
        "location": job.get("location", {}).get("name"),
        "url": job.get("absolute_url"),
        "description": strip_html(job.get("content")),
        "posted_date": job.get("first_published"),
        "source": "greenhouse",
    }


def normalize_lever(job, company_name):
    """Convert one raw Lever job into the common schema.
    company_name is passed in separately since Lever's API never includes it."""
    return {
        "title": job.get("text"),
        "company": company_name,
        "location": job.get("categories", {}).get("location"),
        "url": job.get("hostedUrl"),
        "description": job.get("descriptionPlain"),
        "posted_date": job.get("createdAt"),
        "source": "lever",
    }
