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
    return call_ollama(prompt)


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
