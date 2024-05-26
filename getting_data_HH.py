import requests
from abc import ABC, abstractmethod


class GetInfoHHAbstract(ABC):
    """Абстрактный класс для получения данных о работодателе и его вакансиях с сайта HH.ru через API, а так же записи
    этих данных в таблицу PostgreSQL"""

    @staticmethod
    @abstractmethod
    def get_info(cur, conn):
        """Абстрактный метод для получения данных через API и занесении этих данных в таблицу PostgreSQL"""
        pass


class GetInfoHH(GetInfoHHAbstract):
    """Класс для получения данных о работодателе и его вакансиях с сайта HH.ru через API а так же записи этих данных в
    таблицу PostgreSQL"""

    @staticmethod
    def get_info(cur, conn):
        # id компаний с которыми я буду работать
        id_companies = [1740, 1473866, 3776, 2523, 776314, 4598057, 5599481, 1459249, 614346, 2919210]

        # Запускаю цикл по id, чтобы вывести все вакансии от этих работодателей
        for id_company in id_companies:
            url = f'https://api.hh.ru/vacancies?employer_id={id_company}'
            params = {'page': 0, 'per_page': 99}
            headers = {'User-Agent': 'HH-User-Agent'}
            response = requests.get(url, headers=headers, params=params)
            response_json = response.json()['items']

            # Определяю название компании(как то может более правильно можно это сделать? Подскажите)
            name_company_dict = {1740: 'Яндекс', 1473866: 'Сбербанк-Сервис', 3776: 'МТС', 2523: 'М.Видео-Эльдорадо',
                                 776314: 'Парфюмерно-косметический супермаркет Золотое Яблоко', 4598057: 'УГМК-Телеком',
                                 5599481: 'Сандуны Урал', 1459249: 'Bright Fit', 614346: 'Айдиго',
                                 2919210: 'ГБУЗ Областная больница г. Троицк'}
            name_company = name_company_dict[id_company]

            # Запускаю цикл по полученной информации о вакансиях от определённого работодателя и записываю эти данные
            # в таблицу
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
                conn.commit()
