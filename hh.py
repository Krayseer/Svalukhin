import datetime
import multiprocessing
import pandas as pd
import requests


def get_vacancies_on_page(start, end, global_result: list):
    pages = 20
    for page in range(pages):
        path = f'https://api.hh.ru/vacancies?specialization=1&date_from={start}&date_to={end}&page={page}&per_page=100'
        response = requests.get(path).json()
        for element in response['items']:
            if element['salary'] is not None:
                vacancy = [element['name'], element['salary']['from'], element['salary']['to'],
                           element['salary']['currency'], element['area']['name'], element['published_at']]
            else:
                vacancy = [element['name'], None, None, None, element['area']['name'], element['published_at']]
            global_result.append(vacancy)


def create_data_file():
    result = multiprocessing.Manager().list()
    hours_in_day = 24
    header = ["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"]

    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    date_time = datetime.datetime(yesterday.year, yesterday.month, yesterday.day)
    for hour in range(hours_in_day):
        date_from = date_time + datetime.timedelta(hours=1) if hour > 0 else date_time
        date_to = date_from + datetime.timedelta(hours=1)
        date_time = date_from

        current_start = date_from.strftime('%Y-%m-%dT%H:%M:%S')
        current_end = date_to.strftime('%Y-%m-%dT%H:%M:%S')

        process = multiprocessing.Process(target=get_vacancies_on_page, args=(current_start, current_end, result,))
        process.start()
        process.join()

    dataframe = pd.DataFrame(list(result))
    dataframe.to_csv('data_vacancies_yesterday.csv', header=header, index=False)


if __name__ == "__main__":
    create_data_file()
