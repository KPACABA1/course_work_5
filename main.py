from getting_data_HH import GetInfoHH
from create_table import CreateTable
from working_with_table import DBManager

# здороваюсь с пользователем и показываю какие компании я выбрал для поиска вакансий
print('Привет, мне интересны следующие вакансии:'
      '\n1. Яндекс'
      '\n2. Сбербанк-Сервис'
      '\n3. МТС'
      '\n4. М.Видео-Эльдорадо'
      '\n5. Парфюмерно-косметический супермаркет Золотое Яблоко'
      '\n6. УГМК-Телеком'
      '\n7. Сандуны Урал'
      '\n8. Bright Fit'
      '\n9. Айдиго'
      '\n10. ГБУЗ Областная больница г. Троицк')

# прошу у пользователя создать базу данных и написать её название, предполагая что host=localhost и user=postgres
print('Напишите пожалуйста название базы данных которую вы создали в PostgreSQL')
database = input()
# Прошу пароль пользователя
print("Введите пожалуйста пароль от PostgreSQL")
password = input()
# Предполагаю что user = postgres, а host = localhost, но лучше убедиться
print("Напишите пожалуйста имя пользователя")
user = input()
print("Напишите пожалуйста host")
host = input()

# Спрашиваю у пользователя создал ли он таблицу для своей базы данных или ее необходимо создать
answer_1 = input("Напишите создадим если таблицу ещё не создавали ")
if answer_1 == "создадим":
    CreateTable.create_table(host, database, user, password)

# Вношу в таблицу данные о вакансиях
GetInfoHH.get_info(host, database, user, password)

first = DBManager(host, database, user, password)

# Спрашиваю у пользователя какую функцию вывести
while True:
    answer_3 = input("Какую функцию хотите вывести?(от 1 до 5), если хотите закончить пишите стоп")
    if answer_3 == 1:
        first.get_companies_and_vacancies_count()
    elif answer_3 == 2:
        first.get_all_vacancies()
    elif answer_3 == 3:
        first.get_avg_salary()
    elif answer_3 == 4:
        first.get_vacancies_with_higher_salary()
    elif answer_3 == 5:
        answer_2 = input("Введите слово для поиска по вакансиям")
        first.get_vacancies_with_keyword(answer_2)
