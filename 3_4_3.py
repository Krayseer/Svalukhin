import pandas as pd


def get_average_salary(element, currencies):
    average_salary = list(map(float, list(filter(None, [element.salary_from, element.salary_to]))))
    average = float(int(sum(average_salary) / len(average_salary) *
                        float(currencies[element.salary_currency]))) if len(average_salary) > 0 else None
    return average


file_name = input("Введите название файла: ")
vacancy = input("Введите название профессии: ")
area = input("Введите название региона: ")

currency_name = ["", "AZN", "BYR", "EUR", "GEL", "KGS", "KZT", "RUR", "UAH", "USD", "UZS"]
currency_value = [1, 35.68, 23.91, 59.90, 21.74, 0.76, 0.13, 1, 1.64, 60.66, 0.0055]
currency_to_rub = dict(zip(currency_name, currency_value))

df = pd.read_csv(file_name)

areas = df.groupby('area_name').area_name.count()
total_vacancies = df['name'].count()
percent = total_vacancies / 100
correct_cities = areas[areas > percent].index.tolist()

df = df[df['area_name'].isin(correct_cities)]
df['salary_to'] = df['salary_to'].fillna("")
df['salary_from'] = df['salary_from'].fillna("")
df['salary_currency'] = df['salary_currency'].fillna("")
df.insert(2, 'salary', df.apply(lambda x: get_average_salary(x, currency_to_rub), axis=1))
df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

salaries = df.groupby('area_name')['salary'].mean().apply(lambda x: float(int(x))).sort_values(ascending=False).head(10)
vacancies = df.groupby('area_name')['area_name'].count().sort_values(ascending=False).apply(
    lambda x: str(round(x/total_vacancies * 100, 2)) + "%").head(10)

df = df[(df['name'].str.contains(vacancy) & df['area_name'].str.contains(area))]
df['published_at'] = df['published_at'].apply(lambda x: x[:4])

salaries_profession = df.groupby('published_at')['salary'].mean().apply(lambda x: float(int(x)))
vacancies_profession = df.groupby('published_at')['name'].count()

first = pd.DataFrame({'area_name': salaries.index.tolist(), 'average_salary': salaries.tolist()})
second = pd.DataFrame({'area_name': vacancies.index.tolist(), 'percent_vacancies': vacancies.tolist()})
third = pd.DataFrame({'year': [x for x in range(2003, 2022 + 1)], 'average_salary': salaries_profession.tolist()})
fourth = pd.DataFrame({'year': [x for x in range(2003, 2022 + 1)], 'count_vacancy': vacancies_profession.tolist()})

res = pd.concat([first, second, third, fourth], axis=1)
res.to_html("3_4_3.html", index=False)
