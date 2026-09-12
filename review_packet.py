import os
from datetime import datetime
from tailor import tailor_resume

PACKETS_DIR = "review_packets"


def generate_packet(resume_text, listing):
    """
    Builds a review packet (Markdown file) for one listing:
    the original listing info + tailored bullets + keyword gaps.
    This is a DRAFT for a human to review — nothing here gets sent anywhere.
    """
    tailored_output = tailor_resume(resume_text, listing)

    packet_content = f"""# DRAFT — Review Before Sending

**This is a draft only. Nothing has been submitted. Review and send it yourself.**

## Listing
- **Title:** {listing.get('title')}
- **Company:** {listing.get('company')}
- **Location:** {listing.get('location')}
- **URL:** {listing.get('url')}
- **Source:** {listing.get('source')}

## Tailored Suggestions
{tailored_output}

---
*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} — for review only.*
"""

    os.makedirs(PACKETS_DIR, exist_ok=True)
    safe_company = "".join(c for c in listing.get('company', 'unknown') if c.isalnum())
    safe_title = "".join(c for c in listing.get('title', 'job') if c.isalnum() or c == ' ').strip().replace(' ', '_')
    filename = f"{PACKETS_DIR}/{safe_company}_{safe_title}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(packet_content)

    return filename

from tracker_db import update_status

def mark_as_sent(listing_id):
    """
    Call this after a human has reviewed the packet and actually
    submitted the application themselves. Updates the tracker to 'Applied'.
    """
    update_status(listing_id, "Applied")
    print(f"Listing {listing_id} marked as Applied.")
