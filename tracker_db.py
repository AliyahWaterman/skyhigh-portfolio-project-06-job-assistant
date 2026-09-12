import sqlite3
from datetime import datetime

DB_PATH = "tracker.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Creates the listings table if it doesn't already exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            url TEXT UNIQUE,
            status TEXT DEFAULT 'Saved',
            added_date TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_listing(title, company, location, url):
    """Adds a new listing with status 'Saved'. Ignores it if the URL already exists."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO listings (title, company, location, url, status, added_date) VALUES (?, ?, ?, ?, ?, ?)",
            (title, company, location, url, "Saved", datetime.now().isoformat()),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"[tracker] Already tracking: {title} at {company}")
    finally:
        conn.close()


def update_status(listing_id, new_status):
    """Updates the status of one listing by its id."""
    valid_statuses = {"Saved", "Applied", "Interviewing", "Rejected", "Offer"}
    if new_status not in valid_statuses:
        raise ValueError(f"'{new_status}' is not a valid status. Must be one of: {valid_statuses}")

    conn = get_connection()
    conn.execute("UPDATE listings SET status = ? WHERE id = ?", (new_status, listing_id))
    conn.commit()
    conn.close()


def get_all_listings():
    """Returns every tracked listing as a list of dictionaries."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM listings ORDER BY added_date DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]
