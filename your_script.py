import requests
from bs4 import BeautifulSoup
import json
import os

def get_page_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(separator='\n', strip=True)

        # Base URL for appending words
        base_url = 'https://digitalcareers.infosys.com/global-careers/company-job/description/reqid/'
        
        # Check for words ending with "BR" and append them to the base URL
        words = page_text.split()
        new_urls = []
        for word in words:
            if word.endswith("BR"):
                full_url = base_url + word
                new_urls.append(full_url)
        
        return new_urls
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []

def update_urls(new_urls):
    # Path to the JSON file
    json_file = "urls.json"

    # Load existing data from JSON file or create an empty dictionary
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
    else:
        data = {"urls": []}

    # Flag to track if new URLs were added
    new_entries_added = False

    # Check each new URL and add if it doesn't exist
    for url in new_urls:
        if url not in data["urls"]:
            data["urls"].append(url)
            print(f"Added new URL: {url}")
            new_entries_added = True
        else:
            print(f"URL already exists: {url}")

    # Save updated data back to the JSON file if new entries were added
    if new_entries_added:
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
            print("Updated urls.json with new entries.")
    else:
        print("No new URLs added.")

if __name__ == "__main__":
    url = 'https://digitalcareers.infosys.com/infosys/global-careers?location=USA'
    new_urls = get_page_text(url)
    if new_urls:
        update_urls(new_urls)

