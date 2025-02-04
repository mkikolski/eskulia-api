"""
Moduł odpowiedzialny za pobieranie szczegółowych informacji o lekach ze stron internetowych.

Moduł wykorzystuje web scraping do ekstrakcji danych o lekach z podanych stron internetowych,
normalizując tekst i zapisując pary pytanie-odpowiedź do obiektu Drug.
"""
import requests
import unicodedata
from bs4 import BeautifulSoup

from entities.drug import Drug


def get_drug_details(drug: Drug):
    """
    Pobiera szczegółowe informacje o leku ze strony internetowej.

    Funkcja wykonuje zapytanie HTTP do strony określonej w atrybucie link obiektu Drug,
    następnie parsuje zawartość HTML w poszukiwaniu par pytanie-odpowiedź.
    Znalezione informacje są dodawane do obiektu Drug jako obiekty Detail.

    Args:
        drug (Drug): Obiekt klasy Drug zawierający podstawowe informacje o leku,
            w tym link do strony z dodatkowymi szczegółami.

    Returns:
        None

    Notes:
        - Funkcja szuka elementów <h2> bez klasy oraz następujących po nich
          elementów <div> z klasą 'item-content'
        - Tekst jest normalizowany przy użyciu NFKD (dekompozycja zgodności)
        - W przypadku błędu połączenia lub braku odpowiedzi 200, 
          szczegóły nie zostaną dodane
        - Funkcja modyfikuje przekazany obiekt drug, dodając do niego
          znalezione szczegóły

    Example:
        >>> drug = Drug("Paracetamol", "Przeciwbólowy", "https://example.com/paracetamol")
        >>> get_drug_details(drug)
        >>> print(len(drug.details))  # Wyświetli liczbę znalezionych szczegółów

    Raises:
        requests.RequestException: Może wystąpić w przypadku problemów z połączeniem
        
    Web Scraping Structure:
        Funkcja oczekuje następującej struktury HTML:
        <h2>Pytanie</h2>
        <div class="item-content">Odpowiedź</div>
    """
    # Wykonanie zapytania HTTP
    response = requests.get(drug.link)

    # Sprawdzenie czy odpowiedź jest poprawna
    if response.status_code == 200:
        # Parsowanie zawartości HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Znalezienie wszystkich elementów h2 bez klasy
        h2_elements = soup.find_all('h2', class_=False)

        # Przetwarzanie znalezionych elementów
        for h2 in h2_elements:
            # Szukanie następnego elementu div z klasą 'item-content'
            next_element = h2.find_next_sibling('div', class_='item-content')
            if next_element:
                # Normalizacja tekstu i dodanie szczegółów do obiektu drug
                question = unicodedata.normalize("NFKD", (h2.get_text(strip=True)))
                answer = unicodedata.normalize("NFKD", (next_element.get_text(strip=True)))
                drug.add_detail(question, answer)



