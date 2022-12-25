import os

import pandas as pd
import pdfkit
from separator import get_separate_files

file = input("Введите название файла: ")
vacancy = input("Введите название профессии: ")

get_separate_files(file)

result = {}
header = ["Year",
          "Dynamics of salary levels by years",
          "Dynamics of the number of vacancies by years",
          "Dynamics of the level of salaries by years for the chosen profession",
          "Dynamics of the number of vacancies by years for the chosen profession"]

for head in header:
    result[head] = []

for year in range(2003, 2022 + 1):
    file = f"files/{year}.csv"

    df = pd.read_csv(file)
    average = (df['salary_to'].mean() + df['salary_from'].mean()) / 2
    count = df['name'].count()

    df = df[df['name'].str.contains(vacancy)]
    average_profession = (df['salary_to'].mean() + df['salary_from'].mean()) / 2
    count_profession = df['name'].count()

    result_info = [year, average, count, average_profession, count_profession]
    for i in range(len(header)):
        result[header[i % len(header)]].append(result_info[i % len(header)])

pd.DataFrame(result).to_html('temp.html', index=False)
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_file('temp.html', '3_4_2.pdf', configuration=config, options={"enable-local-file-access": ""})
os.remove("temp.html")
