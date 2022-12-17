import csv

import requests
import pandas as pd
import xmltodict as xmltodict


def get_table_frequency(data):
    header = ["Валюта", "Количество", "Частотность"]
    currencies = []
    for k, v in data.items():
        currencies.append([k, v, round(v / sum(data.values()), 2)])
    dataframe = pd.DataFrame(currencies, columns=header)
    print(dataframe)


def get_correct_currency_frequency(file_name):
    result = {}
    with open(file_name, encoding='utf-8-sig') as file:
        for element in csv.DictReader(file):
            if element['salary_currency'] not in result:
                result[element['salary_currency']] = 0
            result[element['salary_currency']] += 1

    sorted_dic = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    # get_table_frequency(sorted_dic) -- функция для вывода в консоль частотности валют

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
        reader = csv.DictReader(file)
        date_currency = {}
        for row in reader:
            for key, value in row.items():
                date_currency[value.split(';')[0]] = {}
                for index in range(1, len(key.split(';')[1:]) + 1):
                    date_currency[value.split(';')[0]][key.split(';')[index]] = value.split(';')[index]
    return date_currency


def get_processed_information(file_name):
    currency = get_correct_currency_frequency(file_name)
    date_curr = get_currency_by_date_dict("currency_by_month.csv")

    result = []
    with open(file_name, encoding='utf-8-sig') as file:
        for line in csv.DictReader(file):
            if line['salary_currency'] in currency:
                if line['salary_currency'] != "" and line['salary_currency'] != "RUR":
                    ratio = date_curr[line['published_at'][:7]][line['salary_currency']]
                    index = float(ratio) if ratio != "" else 1
                else:
                    index = 1

                info = list(map(float, list(filter(None, [line['salary_from'], line['salary_to']]))))
                salary = float(int(sum(info) / len(info) * index)) if len(info) > 0 else None
                result.append({'name': line['name'], 'salary': salary,
                               'area_name': line['area_name'], 'published_at': line['published_at']})

    dataframe = pd.DataFrame(result)
    dataframe.to_csv('all_vacancies.csv', index=False)

    first_100 = pd.read_csv("all_vacancies.csv", nrows=100)
    first_100.to_csv('first_100.csv', index=False)


get_processed_information("vacancies_dif_currencies.csv")
