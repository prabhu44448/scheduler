import requests
from bs4 import BeautifulSoup
import json
import os
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_page_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text(separator='\n', strip=True)

    base_url = 'https://digitalcareers.infosys.com/global-careers/company-job/description/reqid/'
    words = page_text.split()
    new_urls = {}
    for word in words:
        if word.endswith("BR"):
            full_url = base_url + word
            new_urls[word] = full_url

    return new_urls

def update_urls(new_urls):
    json_file = "urls.json"

    try:
        if os.path.exists(json_file):
            with open(json_file, "r") as file:
                data = json.load(file)
        else:
            data = {}
    except Exception as e:
        logging.error(f"Failed to read JSON file: {e}")
        return

    new_entries_added = False

    for key, url in new_urls.items():
        if key not in data:
            data[key] = url
            print(f"Added new URL: {url}")
            new_entries_added = True
        else:
            print(f"URL already exists for key: {key}")

    if new_entries_added:
        try:
            with open(json_file, "w") as file:
                json.dump(data, file, indent=4)
            print("Updated urls.json with new entries.")
        except Exception as e:
            logging.error(f"Failed to write JSON file: {e}")
    else:
        print("No new URLs added.")

if __name__ == "__main__":
    url = 'https://digitalcareers.infosys.com/infosys/global-careers?location=USA'
    try:
        new_urls = get_page_text(url)
        if new_urls:
            update_urls(new_urls)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
