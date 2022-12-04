import csv

vacancies = dict()
with open("vacancies_by_year.csv", encoding='utf-8-sig') as file:
    for row in csv.DictReader(file):
        correct_row = True
        for field in row:
            if row[field] is None or len(row[field]) == 0:
                correct_row = False
                continue
        if correct_row:
            year = int(row['published_at'][:4])
            if year not in vacancies.keys():
                vacancies[year] = list()
            vacancies[year].append(row)

for year, vac_list in vacancies.items():
    with open(f'files/{year}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=vac_list[0].keys())
        writer.writeheader()
        for vacancy in vac_list:
            writer.writerow(vacancy)
