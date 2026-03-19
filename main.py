import requests
import json
import os
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://www.amazon.jobs/en/search.json?offset=0&result_limit=10&sort=recent&category[]=software-development&country[]=USA"

# 🔹 Fetch jobs from Amazon API
def get_amazon_jobs():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data.get("jobs", [])
    except Exception as e:
        logging.error(f"Failed to fetch jobs: {e}")
        return []

# 🔹 Update JSON and detect new jobs
def update_jobs(jobs):
    json_file = "amazon_jobs.json"

    try:
        if os.path.exists(json_file):
            with open(json_file, "r") as file:
                stored = json.load(file)
        else:
            stored = {}
    except Exception as e:
        logging.error(f"Failed to read JSON: {e}")
        return

    new_jobs = {}

    for job in jobs:
        job_id = str(job["id"])
        job_url = f"https://www.amazon.jobs/en/jobs/{job_id}"

        if job_id not in stored:
            stored[job_id] = {
                "title": job["title"],
                "location": job["location"],
                "posting_date": job.get("posting_date"),
                "url": job_url
            }
            new_jobs[job_id] = stored[job_id]
            print(f"New job found: {job['title']}")
        else:
            print(f"Already exists: {job['title']}")

    if new_jobs:
        try:
            with open(json_file, "w") as file:
                json.dump(stored, file, indent=4)
            print("Updated amazon_jobs.json")
            send_email(new_jobs)
        except Exception as e:
            logging.error(f"Failed to write JSON: {e}")
    else:
        print("No new jobs found.")

# 🔹 Send email
def send_email(new_jobs):
    sender_email = "prabhukiran.chintha@gmail.com"
    receiver_email = "prabhukiran.chintha@gmail.com"
    password = "uoen gjyk fwkt fkqa"

    body = ""
    for job in new_jobs.values():
        body += (
            f"Title: {job['title']}\n"
            f"Location: {job['location']}\n"
            f"URL: {job['url']}\n\n"
        )

    subject = f"New Amazon Jobs - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        logging.error(f"Email failed: {e}")

# 🔹 Main
if __name__ == "__main__":
    try:
        jobs = get_amazon_jobs()
        if jobs:
            update_jobs(jobs)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
