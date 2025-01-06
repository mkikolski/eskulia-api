# api/drug_api.py
import requests
from typing import Optional, Dict, Any

class PolishMedicinesAPI:
    BASE_URL = "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/search/public"
    
    @staticmethod
    def search_drug(code: str) -> Optional[Dict[Any, Any]]:
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