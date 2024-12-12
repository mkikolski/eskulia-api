import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from datetime import datetime


def export_to_xlsx(drugs):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Drugs"

    current_date = datetime.now().strftime("%d-%m-%Y")

    filename = f"{current_date}_drugs.xlsx"

    ws.append(["drug", "type", "link", "detail", "answer"])

    for drug in drugs:
        if not drug.details:
            ws.append([drug.name, drug.type, drug.link, "", ""])
        else:
            for detail in drug.details:
                clean_answer = ILLEGAL_CHARACTERS_RE.sub(r"", detail.answer)

                ws.append([drug.name, drug.type, drug.link, detail.question, clean_answer])

    wb.save(filename)