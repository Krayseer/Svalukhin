import cProfile
import concurrent.futures
import csv
import multiprocessing
import os

currency_name = ["AZN", "BYR", "EUR", "GEL", "KGS", "KZT", "RUR", "UAH", "USD", "UZS"]
currency_value = [35.68, 23.91, 59.90, 21.74, 0.76, 0.13, 1, 1.64, 60.66, 0.0055]
currency_to_rub = dict(zip(currency_name, currency_value))


class DataSet:
    def __init__(self):
        # self.directory_name = input("Введите название директории: ")
        # self.profession_name = input("Введите название профессии: ")
        self.directory_name = 'vacancies'
        self.profession_name = 'Аналитик'
        self.professions = list()
        self.year_collection = multiprocessing.Manager().list()

    def get_info(self, is_profession):
        salary_dict = dict()
        count_dict = dict()
        for profession in self.professions:
            profession.salary_from = int(profession.salary_from)
            profession.salary_to = int(profession.salary_to)

            if profession.get_year() not in salary_dict.keys():
                salary_dict[profession.get_year()] = []

            if is_profession:
                if self.profession_name in profession.name:
                    salary_dict[profession.get_year()].append((profession.salary_from + profession.salary_to) // 2
                                                              * currency_to_rub[profession.salary_currency])
            else:
                salary_dict[profession.get_year()].append(int((profession.salary_from + profession.salary_to) // 2
                                                              * currency_to_rub[profession.salary_currency]))

        for key, value in salary_dict.items():
            salary_dict[key] = int(sum(value) // len(value)) if len(value) != 0 else 0
            count_dict[key] = len(value) if len(value) != 0 else 0

        self.year_collection.append(salary_dict)
        self.year_collection.append(count_dict)

    def get_data(self, file):
        with open(f"vacancies/{file}", 'r', encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                self.professions.append(Profession(*[row[field] for field in row]))
            self.get_info(False)
            self.get_info(True)

    def print_data(self):
        dicts = [dict(), dict(), dict(), dict()]
        messages = ['Динамика уровня зарплат по годам:', 'Динамика количества вакансий по годам:',
                    'Динамика уровня зарплат по годам для выбранной профессии:',
                    'Динамика количества вакансий по годам для выбранной профессии:']
        for index in range(len(self.year_collection)):
            dicts[index % 4] = {**dicts[index % 4], **self.year_collection[index]}
        [print(messages[index % 4], dicts[index % 4]) for index in range(4)]

    def get_info_with_multiprocess(self):
        for file in os.listdir("vacancies"):
            process = multiprocessing.Process(target=self.get_data, args=(file,))
            process.start()
            process.join()
        self.print_data()

    def get_info_without_multiprocess(self):
        for file in os.listdir("vacancies"):
            self.get_data(file)
        self.print_data()

    def get_info_with_concurrent_futures(self):
        for file in os.listdir("vacancies"):
            with concurrent.futures.ProcessPoolExecutor() as executor:
                process = executor.submit(self.get_data, file)
                process.result()
        self.print_data()


class Profession:
    def __init__(self, name, salary_from, salary_to, salary_currency, area_name, published_at):
        self.name = name
        self.salary_from = int(salary_from.replace('.0', ''))
        self.salary_to = int(salary_to.replace('.0', ''))
        self.salary_currency = salary_currency
        self.area_name = area_name
        self.published_at = published_at

    def get_year(self):
        return int(self.published_at[:4])


def execute():
    data_professions = DataSet()
    data_professions.get_info_with_concurrent_futures()


if __name__ == '__main__':
    cProfile.run('execute()')
