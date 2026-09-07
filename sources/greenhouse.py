import requests

def fetch_greenhouse_listings(board_token):
    """
    Fetch job listings from a company's public Greenhouse job board.
    board_token = the company's ID on Greenhouse (e.g. "airbnb", "stripe")
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises an error if the request failed
    except requests.RequestException as e:
        print(f"[greenhouse] Could not reach {board_token}: {e}")
        return []  # dead source handled gracefully — empty list, not a crash

    data = response.json()
    return data.get("jobs", [])
