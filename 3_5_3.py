import sqlite3
import pandas as pd


vacancy_name = input("Введите название профессии: ")
area = input("Введите название региона: ")


def create_sql_from_csv(database):
    dataframe = pd.read_csv("full_vacancies.csv")
    dataframe.published_at = dataframe.published_at.apply(lambda x: x[:-5])
    dataframe.to_sql("vacancies", database, index=False)


db = sqlite3.connect("currency_by_month.db")
cursor = db.cursor()

salary = cursor.execute("""
SELECT STRFTIME('%Y', published_at) AS datetime, ROUND(AVG(salary), 2) FROM vacancies
GROUP BY datetime;
""")
df = pd.DataFrame(salary.fetchall(), columns=['Год', 'Уровень зарплаты'])
df.to_csv("3_5_3_1.csv", index=False)

vacancy = cursor.execute("""
SELECT STRFTIME('%Y', published_at) AS datetime, COUNT(*) FROM vacancies
GROUP BY datetime;
""")
df = pd.DataFrame(vacancy.fetchall(), columns=['Год', 'Количество вакансий'])
df.to_csv("3_5_3_2.csv", index=False)

salary_profession = cursor.execute(f"""
SELECT STRFTIME('%Y', published_at) AS datetime, ROUND(AVG(salary), 2) FROM vacancies
WHERE name LIKE '%{vacancy_name}%' AND area_name LIKE '{area}'
GROUP BY datetime;
""")
df = pd.DataFrame(salary_profession.fetchall(), columns=['Год', f'Уровень зарплаты: {vacancy_name}, {area}'])
df.to_csv("3_5_3_3.csv", index=False)

vacancy_profession = cursor.execute(f"""
SELECT STRFTIME('%Y', published_at) AS datetime, COUNT(*) FROM vacancies
WHERE name LIKE '%{vacancy_name}%' AND area_name LIKE '{area}'
GROUP BY datetime;
""")
df = pd.DataFrame(vacancy_profession.fetchall(), columns=['Год', f'Количество вакансий: {vacancy_name}, {area}'])
df.to_csv("3_5_3_4.csv", index=False)

cities_salary = cursor.execute(f"""
SELECT area_name, ROUND(AVG(salary), 2) FROM vacancies
GROUP BY area_name
HAVING COUNT(area_name) > 22398
ORDER BY AVG(salary) DESC
LIMIT 10;
""")
df = pd.DataFrame(cities_salary.fetchall(), columns=['Город', 'Уровень зарплаты'])
df.to_csv("3_5_3_5.csv", index=False)

cities_vacancy = cursor.execute(f"""
SELECT area_name, ROUND(CAST(COUNT(area_name) AS REAL) / 2239874 * 100, 2) AS percent FROM vacancies
GROUP BY area_name
HAVING COUNT(area_name) > 22398
ORDER BY percent DESC
LIMIT 10
""")
df = pd.DataFrame(cities_vacancy.fetchall(), columns=['Город', 'Доля вакансий'])
df.to_csv("3_5_3_6.csv", index=False)


