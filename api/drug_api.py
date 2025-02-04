"""
Moduł dostępu do API Rejestru Produktów Leczniczych.

Moduł zapewnia interfejs do komunikacji z oficjalnym API Rejestru Produktów
Leczniczych prowadzonym przez eZdrowie, umożliwiając wyszukiwanie leków
po kodach GTIN/EAN.
"""

# api/drug_api.py
import requests
from typing import Optional, Dict, Any

class PolishMedicinesAPI:
    """
    Klasa obsługująca komunikację z API Rejestru Produktów Leczniczych.

    Zapewnia metody do wyszukiwania informacji o lekach w polskim
    rejestrze produktów leczniczych poprzez publiczne API eZdrowie.

    Atrybuty:
        BASE_URL (str): Bazowy adres URL API rejestru produktów leczniczych
    """

    BASE_URL = "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/search/public"
    
    @staticmethod
    def search_drug(code: str) -> Optional[Dict[Any, Any]]:
        """
        Wyszukuje lek w rejestrze na podstawie kodu GTIN/EAN.

        Metoda wysyła zapytanie GET do API rejestru produktów leczniczych,
        próbując znaleźć informacje o leku na podstawie podanego kodu.

        Args:
            code (str): Kod GTIN/EAN leku do wyszukania

        Returns:
            Optional[Dict[Any, Any]]: Słownik zawierający dane o leku w przypadku
                znalezienia, None w przypadku błędu lub braku wyników

        Przykład:
            >>> api = PolishMedicinesAPI()
            >>> result = api.search_drug("5909990123456")
            >>> if result:
            ...     print(f"Znaleziono lek: {result}")
            ... else:
            ...     print("Nie znaleziono leku")
        """
        try:
            # Wyszukiwanie po kodzie GTIN/EAN metodą GET
            response = requests.get(f"{PolishMedicinesAPI.BASE_URL}", params={
                'eanGtin': code
            })
            
            if response.status_code == 200:
                data = response.json()
                return data
            return None
        except Exception as e:
            print(f"Błąd podczas wyszukiwania leku: {e}")
            return None