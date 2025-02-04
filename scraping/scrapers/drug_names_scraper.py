"""
Moduł odpowiedzialny za pobieranie informacji o lekach z serwisu mp.pl.

Moduł zawiera funkcje do pobierania listy URL-i sortowania oraz ekstrakcji
informacji o lekach z poszczególnych stron serwisu medycznego.
"""
import re

import requests
from bs4 import BeautifulSoup

from entities.drug import Drug

def get_sort_by_urls():
    """
    Pobiera listę URL-i do stron z lekami posortowanymi alfabetycznie.

    Funkcja wykonuje zapytanie do strony głównej z lekami i wyodrębnia
    wszystkie linki do podstron z lekami posortowanymi według liter alfabetu.

    Returns:
        list: Lista URL-i do stron z posortowanymi lekami.
            Pusta lista w przypadku błędu lub braku znalezionych linków.

    Notes:
        - Bazowy URL: "https://www.mp.pl/pacjent/leki/items"
        - Funkcja szuka linków w elemencie div z klasą "alphabet-list"
        - W przypadku błędu połączenia zwracana jest pusta lista

    Example:
        >>> urls = get_sort_by_urls()
        >>> print(urls[0])  # Wyświetli pierwszy URL z listy sortowania
        'https://www.mp.pl/pacjent/leki/items.html?letter=A'

    Raises:
        requests.RequestException: Może wystąpić w przypadku problemów z połączeniem
    """
    base_url = "https://www.mp.pl/pacjent/leki/items"

    # Wykonanie zapytania HTTP
    response = requests.get(base_url)
    sort_urls = []

    # Sprawdzenie czy odpowiedź jest poprawna
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Znalezienie listy alfabetycznej i wyodrębnienie linków
        alphabet_list = soup.find("div", class_="alphabet-list")
        sort_urls = [a['href'] for a in alphabet_list.find_all("a", href=True)]

    return sort_urls



def get_drugs_by_page(page_url):
    """
    Pobiera informacje o lekach z określonej strony.

    Funkcja analizuje stronę pod wskazanym URL-em i ekstrahuje informacje
    o lekach, tworząc dla każdego leku obiekt klasy Drug zawierający
    nazwę, typ i link do szczegółowych informacji.

    Args:
        page_url (str): URL strony z listą leków do przeanalizowania.

    Returns:
        list: Lista obiektów Drug zawierających informacje o lekach.
            Pusta lista w przypadku błędu lub braku znalezionych leków.

    Notes:
        - Funkcja wyodrębnia typ leku z nawiasów w nazwie
        - Jeśli typ leku nie jest podany w nawiasach, zostanie ustawiony jako pusty string
        - Funkcja szuka leków w elemencie ul z klasą "list-unstyled drug-list"

    Example:
        >>> drugs = get_drugs_by_page("https://www.mp.pl/pacjent/leki/items.html?letter=A")
        >>> for drug in drugs:
        ...     print(f"{drug.name} ({drug.type})")

    Raises:
        requests.RequestException: Może wystąpić w przypadku problemów z połączeniem

    Pattern:
        Nazwa leku jest analizowana według wzorca: "Nazwa leku (typ leku)"
        Jeśli wzorzec nie zostanie dopasowany, cały tekst jest traktowany jako nazwa
    """
    response = requests.get(page_url)

    # Wykonanie zapytania HTTP
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Znalezienie listy leków
        drug_list = soup.find("ul", class_="list-unstyled drug-list")
        drug_items = drug_list.find_all("a")

        drugs = []
        # Przetwarzanie każdego znalezionego leku
        for item in drug_items:
            full_name = item.text.strip()
            link = item['href']

            # Wyodrębnienie typu leku z nawiasów
            match = re.search(r"\((.*?)\)", full_name)
            if match:
                drug_type = match.group(1)
                name = full_name.replace(f" ({drug_type})", "").strip()
            else:
                name = full_name
                drug_type = ""

            drugs.append(Drug(name, drug_type, link))

        return drugs



