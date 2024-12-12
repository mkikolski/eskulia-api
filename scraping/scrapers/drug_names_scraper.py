import re

import requests
from bs4 import BeautifulSoup

from entities.drug import Drug

def get_sort_by_urls():
    base_url = "https://www.mp.pl/pacjent/leki/items"

    response = requests.get(base_url)
    sort_urls = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        alphabet_list = soup.find("div", class_="alphabet-list")
        sort_urls = [a['href'] for a in alphabet_list.find_all("a", href=True)]

    return sort_urls



def get_drugs_by_page(page_url):
    response = requests.get(page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        drug_list = soup.find("ul", class_="list-unstyled drug-list")
        drug_items = drug_list.find_all("a")

        drugs = []
        for item in drug_items:
            full_name = item.text.strip()
            link = item['href']

            match = re.search(r"\((.*?)\)", full_name)
            if match:
                drug_type = match.group(1)
                name = full_name.replace(f" ({drug_type})", "").strip()
            else:
                name = full_name
                drug_type = ""

            drugs.append(Drug(name, drug_type, link))

        return drugs



