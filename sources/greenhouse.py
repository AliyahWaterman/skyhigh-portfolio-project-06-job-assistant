import requests

def fetch_greenhouse_listings(board_token):
    """
    Fetch job listings from a company's public Greenhouse job board,
    including full job descriptions.
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[greenhouse] Could not reach {board_token}: {e}")
        return []

    data = response.json()
    return data.get("jobs", [])
