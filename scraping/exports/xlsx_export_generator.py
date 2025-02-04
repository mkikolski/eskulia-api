"""
Moduł odpowiedzialny za eksport danych o lekach do pliku Excel.

Moduł zawiera funkcjonalność umożliwiającą zapisywanie informacji o lekach
i ich szczegółach do pliku w formacie .xlsx, z uwzględnieniem czyszczenia
niedozwolonych znaków i automatycznego generowania nazwy pliku z datą.
"""
import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from datetime import datetime


def export_to_xlsx(drugs):
    """
    Eksportuje listę leków do pliku Excel (.xlsx).

    Funkcja tworzy nowy plik Excel zawierający informacje o lekach,
    ich typach, linkach oraz szczegółach w formie pytań i odpowiedzi.
    Nazwa pliku generowana jest automatycznie z aktualną datą.

    Args:
        drugs (list): Lista obiektów klasy Drug do wyeksportowania.
            Każdy obiekt powinien posiadać atrybuty: name, type, link
            oraz details (lista obiektów Detail).

    Returns:
        None

    Notes:
        - Plik zostanie zapisany w bieżącym katalogu
        - Format nazwy pliku: "DD-MM-YYYY_drugs.xlsx"
        - Niedozwolone znaki w odpowiedziach są automatycznie usuwane
        - Jeśli lek nie ma szczegółów, zostanie dodany jeden wiersz
          z pustymi polami detail i answer

    Example:
        >>> drugs = [Drug("Paracetamol", "Przeciwbólowy", "http://example.com")]
        >>> export_to_xlsx(drugs)
        # Tworzy plik "04-02-2025_drugs.xlsx" z danymi leku

    File Structure:
        Utworzony plik Excel będzie zawierał następujące kolumny:
        - drug: nazwa leku
        - type: typ leku
        - link: link do źródła
        - detail: pytanie dotyczące leku
        - answer: odpowiedź na pytanie
    """
    # Tworzenie nowego workbooka
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Drugs"

    # Generowanie nazwy pliku z aktualną datą
    current_date = datetime.now().strftime("%d-%m-%Y")
    filename = f"{current_date}_drugs.xlsx"

    # Dodawanie nagłówków
    ws.append(["drug", "type", "link", "detail", "answer"])

    # Zapisywanie danych o lekach
    for drug in drugs:
        if not drug.details:
            # Jeśli lek nie ma szczegółów, dodaj pusty wiersz
            ws.append([drug.name, drug.type, drug.link, "", ""])
        else:
            # Dla każdego szczegółu dodaj osobny wiersz
            for detail in drug.details:
                clean_answer = ILLEGAL_CHARACTERS_RE.sub(r"", detail.answer)

                ws.append([drug.name, drug.type, drug.link, detail.question, clean_answer])
                
    # Zapisywanie pliku
    wb.save(filename)