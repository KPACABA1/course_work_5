import psycopg2
from abc import ABC, abstractmethod


class DBManagerAbstract(ABC):
    """Абстрактный класс для работы с таблицей PostgreSQL со следующими абстрактными методами:
    __init__ - инициализация, чтобы каждый раз не указывать параметры для подключения к базе данных
    get_companies_and_vacancies_count - получает список всех компаний и количество вакансий у каждой компании
    get_all_vacancies - получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
    ссылки на вакансию
    get_avg_salary - получает среднюю зарплату по вакансиям
    get_vacancies_with_higher_salary - получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
    get_vacancies_with_keyword - получает список всех вакансий, в названии которых содержатся переданные в метод слова,
    например python"""

    @abstractmethod
    def __init__(self):
        """Инициализация параметров для входа"""
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, vacancies):
        pass


class DBManager(DBManagerAbstract):
    """Класс для работы с таблицей PostgreSQL со следующими методами:
        __init__ - инициализация, чтобы каждый раз не указывать параметры для подключения к базе данных
        get_companies_and_vacancies_count - получает список всех компаний и количество вакансий у каждой компании
        get_all_vacancies - получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
        ссылки на вакансию
        get_avg_salary - получает среднюю зарплату по вакансиям
        get_vacancies_with_higher_salary - получает список всех вакансий, у которых зарплата выше средней по всем
        вакансиям
        get_vacancies_with_keyword - получает список всех вакансий, в названии которых содержатся переданные в метод
        слова, например python"""

    def __init__(self, host, database, user, password):
        """Инициализация параметров для входа"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as curr:
                curr.execute("SELECT company, COUNT(*) FROM information GROUP BY company;")
                info = curr.fetchall()
                for i in info:
                    print(i)
        conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию"""
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as curr:
                curr.execute("SELECT * FROM information")
                info = curr.fetchall()
                for i in info:
                    print(i)
        conn.close()

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as curr:
                curr.execute("SELECT AVG(salary_from) FROM information WHERE salary_from > 0")
                info = curr.fetchall()
                print(info)
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM information WHERE salary_from > 69134")
                info = cur.fetchall()
                for i in info:
                    print(i)
        conn.close()

    def get_vacancies_with_keyword(self, vacancies):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        with psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM information WHERE vacancy LIKE '%{vacancies}%'")
                info = cur.fetchall()
                for i in info:
                    print(i)
        conn.close()
