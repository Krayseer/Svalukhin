import sqlite3
import pandas as pd

db = sqlite3.connect("currency_by_month.db")
cursor = db.cursor()


def get_average(element):
    salary = list(map(float, list(filter(None, [element.salary_from, element.salary_to]))))
    if element.salary_currency not in ["", "RUR"]:
        query = cursor.execute(f"SELECT {element.salary_currency} "
                               f"FROM currency WHERE date = '{element.published_at[:7]}'")
        ratio = query.fetchone()[0]
        index = float(ratio) if ratio is not None else 1
    else:
        index = 1
    average = float(int(sum(salary) / len(salary) * index)) if len(salary) > 0 else None
    return average


def get_processed_information(file_name):
    currency = [x[1] for x in cursor.execute("pragma table_info(currency)")]

    df = pd.read_csv(file_name)
    df = df[(df['salary_currency'].isin(currency) | df['salary_currency'].isna())].fillna("")
    df.insert(2, 'salary', df.apply(lambda element: get_average(element), axis=1))
    df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

    df.to_csv("full_vacancies.csv", index=False)

    first_100 = pd.read_csv("full_vacancies.csv", nrows=100)
    first_100.to_csv('3_5_2.csv', index=False)


get_processed_information("vacancies_dif_currencies.csv")
