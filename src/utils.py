import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from config import ROOT_DIR, USER_SET

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
    filename=os.path.join(ROOT_DIR, "logs", "logs.log"),
    encoding="utf-8",
    filemode="w",
)
logger = logging.getLogger("utils")


def read_excel_file(file_path):
    """Считывает файлы XLSX-фомата"""
    logger.info("Запуск функции read_excel_file()")
    try:
        logger.debug(f"Попытка чтения файла {os.path.basename(file_path)}")
        xlsx_file_data = pd.read_excel(file_path)

    except Exception:
        logger.error("Ошибка чтения файла")
        return pd.DataFrame()
    logger.info("Успешное чтение файла")
    return xlsx_file_data


def get_date_info(date_info):
    """Возвращает дату время в формате datetime исходя из полученных данных"""
    logger.info("Запуск функции get_date_info()")
    try:
        logger.debug(f"Попытка преобразования даты {date_info}")
        date = datetime.strptime(date_info, "%Y-%m-%d %H:%M:%S")
    except Exception:
        logger.error("Ошибка преобразования даты")
        date = datetime.now()
    logger.info("Успешное преобразование даты")
    return date


def get_greeting():
    """Возвращает приветствие в зависимости от времени суток"""
    logger.info(("Запуск функции get_greeting()"))
    date_info = datetime.now()
    if date_info.hour < 6:
        return "Доброй ночи"
    elif date_info.hour < 12:
        return "Доброе утро"
    elif date_info.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_date_range(date_info):
    """Возвращает диапозон дат с начала месяца до указанной даты"""
    logger.info(("Запуск функции get_date_range()"))
    start_date = datetime(date_info.year, date_info.month, 1)

    date_range = pd.date_range(min(start_date, date_info), max(start_date, date_info)).strftime("%d.%m.%Y").tolist()
    logger.debug("Диапозон получен")
    return date_range


def get_user_settings():
    """Возвращает данные из файла user_settings.json"""
    logger.info(("Запуск функции get_user_settings()"))
    logger.debug("Чтение файла user_settings.json")
    with open(USER_SET) as file:
        return json.load(file)


def get_exchange_rates():
    """Возвращает курс валют в рублях"""
    logger.info("Запуск функции get_exchange_rates()")
    logger.debug("Получение API_KEY")
    load_dotenv()
    api_key = os.getenv("API_KEY_Layer")

    user_settings = get_user_settings()

    logger.debug("Получение курса валют")
    courses = {}

    for currency in user_settings.get("user_currencies"):
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)

        status_code = response.status_code
        result = response.json()

        if status_code == 200:
            logger.debug(f"Курс {currency} получен")
            courses[currency] = result["rates"]["RUB"]
        else:
            logger.debug(f"Курс {currency} не получен")
            courses[currency] = "No data"

    return courses


def get_stock_data():
    """Возвращает стоимость акций"""
    logger.info("Запуск функции get_stock_data()")
    logger.debug("Получение API_KEY")
    load_dotenv()
    api_key = os.getenv("API_KEY_SP500")

    user_settings = get_user_settings()
    logger.debug("Получение стоимости акции")
    stocks = {}
    for stock in user_settings.get("user_stocks"):
        url = f"https://financialmodelingprep.com/api/v3/quote-short" f"/{stock}?apikey={api_key}"

        response = requests.get(url)
        status_code = response.status_code
        result = response.json()

        if status_code == 200:
            logger.debug(f"Цена акции {stock} получена")
            stocks[stock] = result[0]["price"]
        else:
            logger.debug(f"Цена акции {stock} не получена")
            stocks[stock] = "No data"

    return stocks


def filter_transactions_by_date_range(transactions_info, date_range):
    """Фильтрует транзакции с начала месяца до указанной даты"""
    logger.info("Запуск функции filter_transactions_by_date_range()")
    filtered_transactions_by_date_range: pd.DataFrame = transactions_info[
        transactions_info["Дата платежа"].isin(date_range)
    ]

    return filtered_transactions_by_date_range


def get_card_info(transactions_info):
    """Возвращает информацию о карте"""
    logger.info("Запуск функции get_card_info()")
    filtered_transactions_by_spent: pd.DataFrame = transactions_info.loc[transactions_info["Сумма платежа"] < 0]

    group_by_card = filtered_transactions_by_spent.groupby(["Номер карты"]).agg({"Сумма платежа": "sum"})

    card_info_list = []
    for index, row in group_by_card.iterrows():
        card_info_list.append(
            {
                "last_digits": index[1:],
                "total_spent": abs(round(row["Сумма платежа"], 2)),
                "cashback": abs(round(row["Сумма платежа"] * 0.01, 2)),
            }
        )
        logger.debug(f"Карта {index} получена")

    return card_info_list


def get_top_transactions(transactions_info):
    """Возвращает топ транзакции по сумме платежа"""
    logger.info("Запуск функции get_top_transactions()")
    sorted_by_spent = transactions_info.sort_values("Сумма платежа", ascending=True)

    top_transactions_list = []
    for index, row in sorted_by_spent.iterrows():
        top_transactions_list.append(
            {
                "date": row["Дата платежа"],
                "amount": abs(row["Сумма платежа"]),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
        logger.debug(f"Транзакция {index} получена")

    return top_transactions_list
