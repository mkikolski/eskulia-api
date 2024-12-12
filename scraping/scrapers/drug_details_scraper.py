import requests
import unicodedata
from bs4 import BeautifulSoup

from entities.drug import Drug


def get_drug_details(drug: Drug):
    response = requests.get(drug.link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        h2_elements = soup.find_all('h2', class_=False)

        for h2 in h2_elements:
            next_element = h2.find_next_sibling('div', class_='item-content')
            if next_element:
                question = unicodedata.normalize("NFKD", (h2.get_text(strip=True)))
                answer = unicodedata.normalize("NFKD", (next_element.get_text(strip=True)))
                drug.add_detail(question, answer)



