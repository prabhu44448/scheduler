import requests
from bs4 import BeautifulSoup

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
        for word in words:
            if word.endswith("BR"):
                
                # Construct and print the full URL
                full_url = base_url + word
                print(f"URL: {full_url}")
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

if __name__ == "__main__":
    url = 'https://digitalcareers.infosys.com/infosys/global-careers?location=USA'
    get_page_text(url)
