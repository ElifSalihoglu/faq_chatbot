import requests
from bs4 import BeautifulSoup
import json

def scrape_faq_data(url):
    """
    Scrape FAQ data from the given URL and return it in JSON format.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        faq_sections = soup.select("div[itemprop='mainEntity']")

        faq_data = []
        for section in faq_sections:
            question = section.select_one("h3[itemprop='name']").get_text(strip=True)
            answer = section.select_one("div[itemprop='acceptedAnswer']").get_text(strip=True)
            faq_data.append({"question": question, "answer": answer})

        # Save data to a JSON file
        with open("data/faq_data.json", "w", encoding="utf-8") as file:
            json.dump(faq_data, file, ensure_ascii=False, indent=4)

        return faq_data
    else:
        raise Exception(f"HTTP request failed with status code {response.status_code}")
