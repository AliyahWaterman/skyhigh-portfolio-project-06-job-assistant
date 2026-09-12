import streamlit as st
from tracker_db import init_db, add_listing, update_status, get_all_listings

init_db()

st.title("Job Search Tracker")

# --- Add a new listing manually ---
st.header("Add a listing")
with st.form("add_listing_form"):
    title = st.text_input("Title")
    company = st.text_input("Company")
    location = st.text_input("Location")
    url = st.text_input("URL")
    submitted = st.form_submit_button("Add")
    if submitted and title and company:
        add_listing(title, company, location, url)
        st.success(f"Added {title} at {company}")

# --- Show the pipeline ---
st.header("Your Pipeline")
listings = get_all_listings()

status_filter = st.selectbox(
    "Filter by status",
    ["All", "Saved", "Applied", "Interviewing", "Rejected", "Offer"]
)

if status_filter != "All":
    listings = [job for job in listings if job["status"] == status_filter]

for job in listings:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{job['title']} — {job['company']}")
            st.caption(f"{job['location']} · Added {job['added_date'][:10]}")
            if job["url"]:
                st.markdown(f"[View listing]({job['url']})")
        with col2:
            new_status = st.selectbox(
                "Status",
                ["Saved", "Applied", "Interviewing", "Rejected", "Offer"],
                index=["Saved", "Applied", "Interviewing", "Rejected", "Offer"].index(job["status"]),
                key=f"status_{job['id']}",
            )
            if new_status != job["status"]:
                update_status(job["id"], new_status)
                st.rerun()
