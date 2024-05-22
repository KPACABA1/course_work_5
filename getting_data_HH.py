import requests
import psycopg2
from abc import ABC, abstractmethod


class GetInfoHHAbstract(ABC):
    """Абстрактный класс для получения данных о работодателе и его вакансиях с сайта HH.ru через API, а так же записи
    этих данных в таблицу PostgreSQL"""

    @staticmethod
    @abstractmethod
    def get_info(host, database, user, password):
        """Абстрактный метод для получения данных через API и занесении этих данных в таблицу PostgreSQL"""
        pass


class GetInfoHH(GetInfoHHAbstract):
    """Класс для получения данных о работодателе и его вакансиях с сайта HH.ru через API а так же записи этих данных в
    таблицу PostgreSQL"""

    @staticmethod
    def get_info(host, database, user, password):
        # id компаний с которыми я буду работать
        id_companies = [1740, 1473866, 3776, 2523, 776314, 4598057, 5599481, 1459249, 614346, 2919210]

        # Запускаю цикл по id, чтобы вывести все вакансии от этих работодателей
        for id_company in id_companies:
            url = f'https://api.hh.ru/vacancies?employer_id={id_company}'
            headers = {'User-Agent': 'HH-User-Agent'}
            response = requests.get(url, headers=headers)
            response_json = response.json()['items']

            # Определяю название компании(как то может более правильно можно это сделать? Подскажите)
            name_company = ''
            if id_company == 1740:
                name_company = 'Яндекс'
            elif id_company == 1473866:
                name_company = 'Сбербанк-Сервис'
            elif id_company == 3776:
                name_company = 'МТС'
            elif id_company == 2523:
                name_company = 'М.Видео-Эльдорадо'
            elif id_company == 776314:
                name_company = 'Парфюмерно-косметический супермаркет Золотое Яблоко'
            elif id_company == 4598057:
                name_company = 'УГМК-Телеком'
            elif id_company == 5599481:
                name_company = 'Сандуны Урал'
            elif id_company == 1459249:
                name_company = 'Bright Fit'
            elif id_company == 614346:
                name_company = 'Айдиго'
            elif id_company == 2919210:
                name_company = 'ГБУЗ Областная больница г. Троицк'

            # Начинаю записывать данные в таблицу
            with psycopg2.connect(host=host, database=database, user=user, password=password) as conn:
                with conn.cursor() as cur:

                    # Запускаю цикл по полученной информации о вакансиях от определённого работодателя
                    for vacancy in response_json:
                        # и уже работаю с информацией в зависимости от имеющейся информации о зарплате
                        if vacancy['salary']:
                            # Если есть информация о стартовой и максимальной заработной плате
                            if vacancy['salary']['from'] and vacancy['salary']['to']:
                                cur.execute("INSERT INTO information VALUES (%s, %s, %s, %s, %s)",
                                            [name_company, vacancy['name'], vacancy['salary']['from'],
                                             vacancy['salary']['to'], vacancy['alternate_url']])
                            # Если есть информация только о стартовой зарплате
                            elif vacancy['salary']['from']:
                                cur.execute("INSERT INTO information VALUES (%s, %s, %s, %s, %s)",
                                            [name_company, vacancy['name'], vacancy['salary']['from'], 0,
                                             vacancy['alternate_url']])
                            # Если есть информация только о максимальной зарплате
                            elif vacancy['salary']['to']:
                                cur.execute("INSERT INTO information VALUES (%s, %s, %s, %s, %s)",
                                            [name_company, vacancy['name'], 0, vacancy['salary']['to'],
                                             vacancy['alternate_url']])
                        # Если вообще информация о зарплате не указана
                        else:
                            cur.execute("INSERT INTO information VALUES (%s, %s, %s, %s, %s)",
                                        [name_company, vacancy['name'], 0, 0,
                                         vacancy['alternate_url']])
            conn.close()
