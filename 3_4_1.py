import csv
import requests
import pandas as pd
import xmltodict as xmltodict


def get_correct_currency_frequency(file_name):
    result = {}
    with open(file_name, encoding='utf-8-sig') as file:
        for element in csv.DictReader(file):
            if element['salary_currency'] not in result:
                result[element['salary_currency']] = 0
            result[element['salary_currency']] += 1
    sorted_dic = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    return dict((k, v) for k, v in sorted_dic.items() if v > 5000)


def create_file_of_correct_data(file_name):
    dates = []
    with open(file_name, encoding='utf-8-sig') as file:
        correct_data = get_correct_currency_frequency(file_name)
        [dates.append(line['published_at']) for line in csv.DictReader(file) if line['salary_currency'] in correct_data]

    correct_vacancies = []
    for year in range(int(min(dates)[:4]), int(max(dates)[:4]) + 1):
        for month in [f'{x:02}' for x in range(1, 13)]:
            response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month}/{year}')
            response_info = xmltodict.parse(response.content)
            vacancy = {'date': f'{year}-{month}'}
            for index in response_info['ValCurs']['Valute']:
                if index['CharCode'] in correct_data:
                    nominal = float(index['Nominal'].replace(',', '.'))
                    value = float(index['Value'].replace(',', '.'))
                    vacancy[index['CharCode']] = round(value / nominal, 7)
            correct_vacancies.append(vacancy)

    dataframe = pd.DataFrame(correct_vacancies)
    dataframe.to_csv("currency_by_month.csv", index=False)


def get_currency_by_date_dict(file_name):
    with open(file_name, encoding='utf-8-sig') as file:
        date_currency = {}
        for row in csv.DictReader(file):
            date_currency[row['date']] = row
    return date_currency


def get_average_salary(element, dict_currency):
    salary = list(map(float, list(filter(None, [element.salary_from, element.salary_to]))))
    if element.salary_currency not in ["", "RUR"]:
        ratio = dict_currency[element.published_at[:7]][element.salary_currency]
        index = float(ratio) if ratio != "" else 1
    else:
        index = 1
    average = float(int(sum(salary) / len(salary) * index)) if len(salary) > 0 else None
    return average


def get_processed_information(file_name):
    currency = list(get_correct_currency_frequency(file_name).keys())
    date_curr = get_currency_by_date_dict("currency_by_month.csv")

    df = pd.read_csv(file_name)
    df = df[(df['salary_currency'].isin(currency) | df['salary_currency'].isna())].fillna("")
    df.insert(2, 'salary', df.apply(lambda element: get_average_salary(element, date_curr), axis=1))
    df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])

    df.to_csv("all_vacancies.csv", index=False)

    first_100 = pd.read_csv("all_vacancies.csv", nrows=100)
    first_100.to_csv('3_4_1.csv', index=False)


get_processed_information("vacancies_dif_currencies.csv")
