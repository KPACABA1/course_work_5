from abc import ABC, abstractmethod


class DBManagerAbstract(ABC):
    """Абстрактный класс для работы с таблицей PostgreSQL со следующими абстрактными методами:
    __init__ - инициализация
    create_table - метод для создания таблицы в уже созданной базе данных
    get_companies_and_vacancies_count - получает список всех компаний и количество вакансий у каждой компании
    get_all_vacancies - получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
    ссылки на вакансию
    get_avg_salary - получает среднюю зарплату по вакансиям
    get_vacancies_with_higher_salary - получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
    get_vacancies_with_keyword - получает список всех вакансий, в названии которых содержатся переданные в метод слова,
    например python"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_table(self):
        """Абстрактный метод для создания таблицы в уже созданной базе данных"""
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
        create_table - Метод для создания таблицы в уже созданной базе данных с 5 колонками
        get_companies_and_vacancies_count - получает список всех компаний и количество вакансий у каждой компании
        get_all_vacancies - получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
        ссылки на вакансию
        get_avg_salary - получает среднюю зарплату по вакансиям
        get_vacancies_with_higher_salary - получает список всех вакансий, у которых зарплата выше средней по всем
        вакансиям
        get_vacancies_with_keyword - получает список всех вакансий, в названии которых содержатся переданные в метод
        слова, например python"""

    def __init__(self, cur, conn):
        self.cur = cur
        self.conn = conn

    def create_table(self):
        """Метод для создания таблицы в уже созданной базе данных с 5 колонками:
        company - название компании
        vacancy - название вакансии
        salary_from - стартовая зарплата
        salary_to - максимальная зарплата
        link - ссылка на вакансию
        Если таблица уже была создана она удаляется и создается заново"""

        self.cur.execute("CREATE TABLE IF NOT EXISTS information (company varchar(55), vacancy varchar(100), "
                         "salary_from int, salary_to int, link text);")
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute("SELECT company, COUNT(*) FROM information GROUP BY company;")
        info = self.cur.fetchall()
        for i in info:
            print(i)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию"""
        self.cur.execute("SELECT * FROM information")
        info = self.cur.fetchall()
        for i in info:
            print(i)

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        self.cur.execute("SELECT AVG(salary_from) FROM information WHERE salary_from > 0")
        info = self.cur.fetchall()
        print(info)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.cur.execute("SELECT * FROM information WHERE salary_from > 69134")
        info = self.cur.fetchall()
        for i in info:
            print(i)

    def get_vacancies_with_keyword(self, vacancies):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        self.cur.execute(f"SELECT * FROM information WHERE vacancy LIKE '%{vacancies}%'")
        info = self.cur.fetchall()
        for i in info:
            print(i)
