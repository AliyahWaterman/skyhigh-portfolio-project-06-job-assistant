import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env into the environment

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def build_prompt(resume_text, listing):
    return f"""You are helping tailor a resume to a specific job listing.

BASE RESUME:
{resume_text}

JOB LISTING:
Title: {listing.get('title')}
Company: {listing.get('company')}
Description: {listing.get('description')}

TASK:
First, check: does this listing actually relate to the candidate's real
background (cloud/DevOps/infrastructure)? If the listing is for an unrelated
field (e.g. fraud investigation, sales, legal, marketing) respond with
exactly: "NOT RELEVANT: this listing does not match the candidate's background."
and nothing else.

If it IS relevant, then:
1. Suggest 3-5 tailored resume bullet points using ONLY real experience found
   in the BASE RESUME above. Do not invent job duties, tools, frameworks, or
   accomplishments that are not explicitly present in the resume text.
2. List keyword gaps: skills mentioned in the JOB LISTING that do NOT appear
   in the BASE RESUME. Only list a gap if you can point to the exact word in
   the listing. If none, say "No significant gaps found."

Respond in this exact format:
BULLETS:
- ...

KEYWORD GAPS:
- ...
"""



def call_ollama(prompt):
    """Sends the prompt to the locally-running Ollama model and returns its reply."""
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]

def tailor_resume(resume_text, listing):
    prompt = build_prompt(resume_text, listing)
    raw_output = call_ollama(prompt)
    return clean_tailored_output(raw_output)


def find_relevant_listing(listings, keywords):
    """
    Returns the first listing whose TITLE (not description) mentions
    at least one of the given keywords. Title-only matching avoids
    false positives from incidental words buried in long descriptions.
    """
    for job in listings:
        title = (job.get("title") or "").lower()
        if any(keyword.lower() in title for keyword in keywords):
            return job
    return None


def clean_tailored_output(raw_output):
    """
    Cleans up the AI's raw output — removes empty bullet lines
    (a known quirk of smaller local models leaving blank '-' placeholders).
    """
    lines = raw_output.split("\n")
    cleaned_lines = [line for line in lines if line.strip() not in ("-", "")]

    # If the KEYWORD GAPS section ended up with nothing real under it, say so explicitly
    if "KEYWORD GAPS:" in raw_output:
        gaps_section = raw_output.split("KEYWORD GAPS:")[1]
        if not any(line.strip().startswith("-") and len(line.strip()) > 1 for line in gaps_section.split("\n")):
            bullets_part = "\n".join(cleaned_lines).split("KEYWORD GAPS:")[0]
            return f"{bullets_part}KEYWORD GAPS:\n- No significant gaps found."

    return "\n".join(cleaned_lines)
