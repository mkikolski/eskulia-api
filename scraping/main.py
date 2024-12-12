import time

from exports.xlsx_export_generator import export_to_xlsx
from scrapers.drug_details_scraper import get_drug_details
from scrapers.drug_names_scraper import get_sort_by_urls, get_drugs_by_page

start_time = time.time()


urls = get_sort_by_urls()

drugs = []
for url in urls:
    drugs += get_drugs_by_page(url)

print("downloaded basic drugs info")
print()

total_drugs = len(drugs)

for idx, drug in enumerate(drugs, start=1):
    get_drug_details(drug)
    if idx % 10 == 0:
        print(f'Processing drug {idx}/{total_drugs}...')

print("downloaded drugs details")
print()

export_to_xlsx(drugs)

print("exported to xlsx file")
print()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")
