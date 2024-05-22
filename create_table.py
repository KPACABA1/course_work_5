from abc import ABC, abstractmethod
import psycopg2


class CreateTableAbstract(ABC):
    """Абстрактный класс для подключения создания таблицы PostgreSQL"""

    @staticmethod
    @abstractmethod
    def create_table(host, database_, user, password):
        """Абстрактный метод для создания таблицы в уже созданной базе данных"""
        pass


class CreateTable(CreateTableAbstract):
    """Класс для создания таблицы PostgreSQL"""

    @staticmethod
    def create_table(host, database, user, password):
        """Метод для создания таблицы в уже созданной базе данных с 5 колонками:
        company - название компании
        vacancy - название вакансии
        salary_from - стартовая зарплата
        salary_to - максимальная зарплата
        link - ссылка на вакансию"""

        # Подключаюсь к указанной базе данных и создаю в ней таблицу с 5 колонками
        with psycopg2.connect(host=host, database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE information (company varchar(55), vacancy varchar(100), "
                            "salary_from int, salary_to int, link text);")
        conn.close()
