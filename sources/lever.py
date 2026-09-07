import requests

def fetch_lever_listings(company_slug):
    """
    Fetch job listings from a company's public Lever job board.
    company_slug = the company's ID on Lever (e.g. "netflix", "canva")
    """
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[lever] Could not reach {company_slug}: {e}")
        return []

    return response.json()
