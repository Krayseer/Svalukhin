import csv


def get_separate_files(file_name):
    vacancies = dict()
    with open(file_name, encoding='utf-8-sig') as file:
        for row in csv.DictReader(file):
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
