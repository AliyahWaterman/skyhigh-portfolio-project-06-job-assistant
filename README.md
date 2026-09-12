# SoleCloud Job Search Assistant

A local-first tool that helps job seekers find relevant listings, generate genuinely tailored resume suggestions, and track their application pipeline — without ever auto-submitting an application. A human always reviews and sends.

## Why this exists

Job hunting at scale is tedious: fifteen applications a week, the same resume pasted everywhere, no memory of who replied. This tool automates the tedious parts — finding listings, tailoring materials, tracking status — and stops deliberately before the "submit" button. That stopping point is the whole point of the design, not a limitation of it.

## Architecture

**Data flow:**

1. `sources/greenhouse.py` + `sources/lever.py` — fetch raw listings from company job boards
2. `sources/normalize.py` — reshape both into one common format
3. `dedupe.py` — remove duplicate listings
4. `app.py` (Streamlit) — browse listings, save the ones you like to `tracker.db`
5. `tailor.py` — generate tailored resume bullets for a chosen listing, using a local AI model (Ollama)
6. `review_packet.py` — package the listing + tailored bullets into a Markdown draft file
7. **A human reviews the draft, applies on the real site manually**
8. `mark_as_sent()` — updates the tracker to "Applied," only after the human confirms they actually sent it

```
[Greenhouse API] ─┐
                   ├──▶ normalize + dedupe ──▶ tracker.db (SQLite)
[Lever API]     ───┘                                │
                                                      ▼
                                          Streamlit app (browse/save)
                                                      │
                                                      ▼
                                          tailor.py (local AI model)
                                                      │
                                                      ▼
                                    review_packet.py → Markdown DRAFT
                                                      │
                                                      ▼
                              HUMAN reviews, applies manually,
                                 then calls mark_as_sent()
```

**Flow:** `main.py` pulls listings from configured sources → normalizes and dedupes them → `app.py` (Streamlit) lets you browse and save ones you like to `tracker.db` → `tailor.py` generates tailored suggestions for a chosen listing using a local AI model → `review_packet.py` packages that into a Markdown draft → you review it, apply on the real site yourself, then call `mark_as_sent()` to update your tracker.

## Generic Plumbing vs. Role-Specific Logic

This project is split so someone targeting a completely different role could reuse most of it:

**Generic (reusable as-is):**
- `sources/` — Greenhouse and Lever API fetchers work for any company/role
- `dedupe.py` — deduplication logic is role-agnostic
- `tracker_db.py` and `app.py` — the tracker and UI don't care what role you're tracking
- `review_packet.py` — packet generation and the human-review gate apply to any tailoring output
- `tailor.py`'s API-calling mechanics (`call_ollama`) — the *plumbing* of talking to the AI

**Role-specific (swap this out for a different target):**
- `config.py` — which companies to pull from
- `data/base_resume.txt` — your actual resume content
- `research/ROLE-RESEARCH.md` — the target role research from Ticket 0
- `tailor.py`'s `build_prompt()` function — the instructions given to the AI are generic in structure, but you may want to adjust tone/emphasis for a very different field (e.g. creative roles vs. technical roles)

## How to Adapt This for a Different Role

1. Redo Ticket 0's research for your new target role — update `research/ROLE-RESEARCH.md` with new keywords and a new target profile
2. Replace `data/base_resume.txt` with a resume relevant to that role
3. Update `config.py` with company slugs relevant to that field
4. Review `build_prompt()` in `tailor.py` — the anti-fabrication and relevance-check instructions stay the same, but you may want to adjust the tone of what counts as "relevant" keywords for the relevance filter
5. Everything else — sources, dedup, tracker, review packet, human-review gate — works unchanged

## Setup & Run Instructions

```bash
# 1. Clone the repo
git clone https://github.com/AliyahWaterman/skyhigh-portfolio-project-06-job-assistant.git
cd skyhigh-portfolio-project-06-job-assistant

# 2. Set up your environment file
cp .env.example .env
# (Ollama needs no real secrets, but this is the pattern if you add a paid API key later)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Ollama and pull a free local model (one-time)
# See https://ollama.com — then run:
ollama run llama3.2

# 5. Run the listing aggregator
python main.py

# 6. Launch the tracker UI
python -m streamlit run app.py

# 7. Generate a review packet for a chosen listing (see review_packet.py)
```

## Where Automation Stops, and Why

This tool automates everything up to the point of submission: finding listings, tailoring resume language, tracking pipeline status, and packaging a clean review draft. It deliberately does **not** auto-apply. Every major job platform bans automated application submission in their terms of service, and a robotically-submitted application under a real person's name is both a policy violation and a bad signal to employers. More importantly, a human should always be the one deciding what gets sent on their behalf — tailored language needs a final sanity check, and a job application is a real commitment that shouldn't happen without a person consciously making it. The `mark_as_sent()` function exists specifically to require a deliberate, manual action before the tracker reflects an application as sent.
