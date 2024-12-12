import os
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

CSV_URL = os.getenv("CSV_URL", "https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/get-csv")  
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "test")
DB_PASSWORD = os.getenv("DB_PASSWORD", "haslo")
TABLE_NAME = os.getenv("TABLE_NAME", "medicinal_products")


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
        # Łączzenie się z bazą danych
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()

        # Usunięcie istniejącj tabeli, jeśli istnieje
        # cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
        # conn.commit()

        # Wczytanie danych z pliku CSV do DataFrame
        df = pd.read_csv(csv_file, delimiter=';', nrows=10)

        # Przypisanie wszystkim kolumnom typu TEXT
        columns = [f'"{col}" TEXT' for col in df.columns]

        columns_sql = ", ".join(columns)
        create_table_query = f"""
        CREATE TABLE {TABLE_NAME} (
            {columns_sql}
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Tabela {TABLE_NAME} została utworzona na nowo.")

        # Zamkniecie połączenia
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Błąd podczas tworzenia tabeli: {e}")



def update_database(csv_file):
    """Zaktualizuj bazę danych PostgreSQL danymi z pliku CSV."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()

        df = pd.read_csv(csv_file, delimiter=';')

        # przekształcenie wszystkich wartości na tekst, aby uniknąć problemów z typami danych
        df = df.astype(str)

        # Przekształcenie danych na listę krotek
        records = df.values.tolist()

        # Przygotowywanie zapytania
        columns = ", ".join([f'"{col}"' for col in df.columns])  # zaznacznie nazw kolumn w cudzysłowach
        values_placeholder = ", ".join(["%s"] * len(df.columns))

        # Czyszczenie tabeli 
        cursor.execute(f"TRUNCATE TABLE {TABLE_NAME};")

        # Nowe dane
        execute_values(
            cursor,
            f"INSERT INTO {TABLE_NAME} ({columns}) VALUES %s",
            records
        )

        # Zatwierdzenie zmian i zamknięcie
        conn.commit()
        cursor.close()
        conn.close()
        print("Baza danych została zaktualizowana.")
    except Exception as e:
        print(f"Błąd podczas aktualizacji bazy danych: {e}")


def main():
    """Główny workflow: Pobierz plik CSV i zaktualizuj bazę danych."""
    try:
        csv_file = download_csv(CSV_URL)
        # csv_file = "/Users/wiktoriapabis/Downloads/Rejestr_Produktow_Leczniczych_calosciowy_stan_na_dzien_20241218-2.csv"
        create_table_if_not_exists(csv_file)  
        update_database(csv_file)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()



# TAKIEGO POLECENIA UZYJCIE DLA ZBUDOWANIA OBRAZU
# docker build -t my-python-cron-image . 

# uruchomienie kontenera zbudowanego z obrazu
# docker run -it --name my-python-cron-container my-python-cron-image bash

# sprawdzenie czy cron jest uruchomiony
# ps aux | grep cron

# wlaczenie uslugi cron w systemie
# service cron start

# wyświetla aktualnie zaplanowane zadania cron
# crontab -l 




