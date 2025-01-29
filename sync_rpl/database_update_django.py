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


CSV_URL = os.getenv("CSV_URL", "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/get-csv")  

def download_csv(url):
    """Pobiera plik CSV z zewnętrznego źródła."""
    response = requests.get(url)
    if response.status_code == 200:
        with open("data.csv", "wb") as f:
            f.write(response.content)
        print("Plik CSV został pobrany.")
        return "data.csv"
    else:
        raise Exception(f"Nie udało się pobrać pliku CSV. Kod statusu: {response.status_code}")


def create_table_if_not_exists(csv_file):
    """Tworzy tabelę w bazie danych na podstawie struktury pliku CSV."""
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
    """Aktualizuje bazę danych PostgreSQL danymi z pliku CSV."""
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
    """Pobiera plik CSV i aktualizuje bazę danych."""
    try:
        csv_file = download_csv(CSV_URL)
        create_table_if_not_exists(csv_file)  
        update_database(csv_file)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
