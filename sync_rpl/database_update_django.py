"""
Moduł do synchronizacji danych leków z Rejestru Produktów Leczniczych.

Moduł pobiera dane w formacie CSV z oficjalnego rejestru leków,
przetwarza je i aktualizuje bazę danych Django. Obsługuje automatyczną
synchronizację danych o lekach, włączając ich identyfikatory, nazwy,
składniki aktywne i inne istotne informacje.
"""
import os
import requests
import pandas as pd
import django
import sys
from .models import Medicine


# sys.path.append('/Users/wiktoriapabis/Desktop/Projekt_grupowy/eskulia-api')

# os.chdir('/Users/wiktoriapabis/Desktop/Projekt_grupowy/eskulia-api')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eskuliaapi.settings")
django.setup()

# URL do pliku CSV z danymi o lekach
CSV_URL = os.getenv("CSV_URL", "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/get-csv")  

def download_csv(url):
    """
    Pobiera plik CSV z zewnętrznego źródła i zapisuje lokalnie.

    Args:
        url (str): Adres URL, z którego ma zostać pobrany plik CSV.

    Returns:
        str: Nazwa zapisanego pliku CSV ('data.csv').

    Raises:
        Exception: Gdy nie uda się pobrać pliku (kod statusu != 200).

    Example:
        >>> csv_file = download_csv(CSV_URL)
        >>> print(f"Plik został zapisany jako: {csv_file}")

    Notes:
        - Plik jest zapisywany w bieżącym katalogu jako 'data.csv'
        - W przypadku istniejącego pliku zostanie on nadpisany
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open("data.csv", "wb") as f:
            f.write(response.content)
        print("Plik CSV został pobrany.")
        return "data.csv"
    else:
        raise Exception(f"Nie udało się pobrać pliku CSV. Kod statusu: {response.status_code}")


def create_table_if_not_exists(csv_file):
    """
    Weryfikuje zgodność struktury bazy danych z formatem pliku CSV.

    Funkcja sprawdza, czy wszystkie kolumny z pliku CSV mają odpowiadające
    im pola w modelu Medicine. Służy jako zabezpieczenie przed zmianami
    w strukturze danych źródłowych.

    Args:
        csv_file (str): Ścieżka do pliku CSV do przeanalizowania.

    Raises:
        Exception: Gdy wystąpi błąd podczas analizy pliku lub weryfikacji struktury.

    Notes:
        - Funkcja wczytuje tylko pierwsze 10 wierszy do analizy struktury
        - Nie wprowadza zmian w strukturze bazy danych
        - Służy głównie do celów weryfikacyjnych

    Example:
        >>> create_table_if_not_exists('data.csv')
        "Tabela medicines została sprawdzona."
    """
    try:
        df = pd.read_csv(csv_file, delimiter=';', nrows=10)

        columns = [f'"{col}" TEXT' for col in df.columns]

        for col in df.columns:
            if not Medicine._meta.get_field(col):
                pass  

        print(f"Tabela {Medicine._meta.db_table} została sprawdzona.")
        
    except Exception as e:
        print(f"Błąd podczas tworzenia tabeli: {e}")


def update_database(csv_file):
    """
    Aktualizuje bazę danych danymi z pliku CSV.

    Funkcja czyści obecne rekordy i wprowadza nowe dane z pliku CSV.
    Wykorzystuje bulk_create dla efektywnego wprowadzania danych.

    Args:
        csv_file (str): Ścieżka do pliku CSV z danymi do importu.

    Raises:
        Exception: Gdy wystąpi błąd podczas przetwarzania pliku lub aktualizacji bazy.

    Notes:
        - Wszystkie istniejące rekordy są usuwane przed importem
        - Wszystkie wartości są konwertowane na typ string
        - Wykorzystuje bulk_create dla lepszej wydajności
        - Obsługuje brakujące wartości, zastępując je pustymi stringami

    Example:
        >>> update_database('data.csv')
        "Baza danych została zaktualizowana."
    """
    try:
        df = pd.read_csv(csv_file, delimiter=';')

        df = df.astype(str)

        Medicine.objects.all().delete()

        medicine_records = []
        for _, row in df.iterrows():
            print(df.head())
            medicine_records.append(Medicine(
                identyfikator=row['identyfikator'],
                nazwa=row['nazwa'],
                nazwa_powszechna=row.get('nazwa_powszechna', ''),
                rodzaj_preparatu=row.get('rodzaj_preparatu', ''),
                droga_podania=row.get('droga_podania', ''),
                moc=row.get('moc', ''),
                postac_farmaceutyczna=row.get('postac_farmaceutyczna', ''),
                kod_atc=row.get('kod_atc', ''),
                podmiot_odpowiedzialny=row.get('podmiot_odpowiedzialny', ''),
                substancja_czynna=row.get('substancja_czynna', '')
            ))

        Medicine.objects.bulk_create(medicine_records)

        print("Baza danych została zaktualizowana.")
    except Exception as e:
        print(f"Błąd podczas aktualizacji bazy danych: {e}")


def main():
    """
    Główna funkcja wykonawcza modułu.

    Koordynuje proces pobierania danych i aktualizacji bazy danych.
    Wykonuje kolejno:
    1. Pobranie pliku CSV
    2. Sprawdzenie struktury bazy danych
    3. Aktualizację danych

    Raises:
        Exception: Gdy wystąpi błąd w którymkolwiek z etapów procesu.

    Example:
        >>> main()
        "Plik CSV został pobrany."
        "Tabela medicines została sprawdzona."
        "Baza danych została zaktualizowana."
    """
    try:
        csv_file = download_csv(CSV_URL)
        create_table_if_not_exists(csv_file)  
        update_database(csv_file)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
