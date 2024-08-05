from src.reports import spending_by_category
from src.services import simple_search
from src.utils import get_date_info
from src.views import get_main_page_info

# приветствие
print(
    """Здравствуйте!
Для получения информации, пожалуйста, введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"""
)
# запрос даты
date = (
    f"{int(input("Год: "))}-{int(input("Месяц: "))}-{int(input("День: "))} "
    f"{int(input("Часы: "))}:{int(input("Минуты: "))}:{int(input("Секунды: "))}"
)

repit = "д"
# выбор действия
while repit == "д":
    print("\nКакую информацию вы хотите получить?\n")
    print("1. Информацию с главной страницы")
    print("2. Результаты поиска по категории и описанию")
    print("3. Отчёт трат по выбранной категории")
    print("4. Всю вышеперечисленную информацию\n")

    try:
        answer = int(input("Введите цифру: \n"))
    except ValueError:
        print("Некорректный ввод. Выбран пункт 4\n")
        answer = 4

    # получение информации исходя из запроса пользователя
    if answer == 1:
        get_main_page_info(date)

    elif answer == 2:
        word = input("Введите слово для поиска: ").strip()
        simple_search(word)

    elif answer == 3:
        category = input("Введите назавание категории: ").strip().capitalize()
        date_info = get_date_info(date)
        spending_by_category(category, date=date_info)

    elif answer == 4:
        get_main_page_info(date)
        word = input("Введите слово для поиска по категории и описанию: ").strip()
        simple_search(word)
        category = input("Введите назавание категории: ").strip().capitalize()
        date_info = get_date_info(date)
        spending_by_category(category, date=date_info)

    else:
        print("Некорректный ввод. Выбран пункт 4\n")
        get_main_page_info(date)
        word = input("Введите слово для поиска по категории и описанию: ").strip()
        simple_search(word)
        category = input("Введите назавание категории: ").strip().capitalize()
        date_info = get_date_info(date)
        spending_by_category(category, date=date_info)

    repit = input("Хотите получить другую информацию? (д/н): \n").strip().lower()

    if repit == "д":
        continue

print("До свидания!")
