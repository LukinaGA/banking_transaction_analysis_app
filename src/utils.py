import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv


def read_excel_file(file_path):
    """Считывает файлы XLSX-фомата"""
    try:
        xlsx_file_data = pd.read_excel(file_path)

    except Exception:
        return None

    return xlsx_file_data


def greeting(date_info):
    """Возвращает приветствие в зависимости от времени суток"""
    if date_info.hour < 6:
        return "Доброй ночи"
    elif date_info.hour < 12:
        return "Доброе утро"
    elif date_info.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_date_range(user_date):
    """Возвращает диапозон дат с начала месяца до указанной даты"""
    start_date = datetime(user_date.year, user_date.month, 1)
    end_date = user_date

    date_range = pd.date_range(min(start_date, end_date), max(start_date, end_date)).strftime('%d.%m.%Y').tolist()

    return date_range


def get_exchange_rates():
    """Возвращает курс валют в рублях"""
    load_dotenv()
    api_key = os.getenv("API_KEY_Layer")

    with open("..\\user_settings.json") as file:
        user_settings = json.load(file)

    courses = {}

    for currency in user_settings["user_currencies"]:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)

        status_code = response.status_code
        result = response.json()

        if status_code == 200:
            courses[currency] = result["rates"]["RUB"]

    return courses


def get_stock_data():
    """Возвращает стоимость акций"""
    load_dotenv()
    api_key = os.getenv("API_KEY_SP500")

    with open("..\\user_settings.json") as file:
        user_settings = json.load(file)

    stocks = {}

    for stock in user_settings["user_stocks"]:
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{stock}?apikey={api_key}"

        response = requests.get(url)
        status_code = response.status_code
        result = response.json()

        if status_code == 200:
            stocks[stock] = result[0]["price"]

    return stocks


def filter_transactions_by_date_range(transactions_info, date_range):
    """Фильтрует транзакции с начала месяца до указанной даты"""
    filtered_transactions_by_date_range: pd.DataFrame = transactions_info.loc[
        transactions_info["Дата платежа"].isin(date_range)]

    return filtered_transactions_by_date_range


def get_card_info(transactions_info):
    """Возвращает информацию о карте"""
    filtered_transactions_by_spent: pd.DataFrame = transactions_info.loc[
        transactions_info["Сумма операции"] < 0]

    group_by_card = filtered_transactions_by_spent.groupby(["Номер карты"]).agg({"Сумма платежа": "sum"})

    card_info_list = []
    for index, row in group_by_card.iterrows():
        card_info_list.append({
            "last_digits": index[1:],
            "total_spent": abs(round(row["Сумма платежа"], 2)),
            "cashback": abs(round(row["Сумма платежа"] * 0.01, 2))
        })

    return card_info_list


def get_top_transactions(transactions_info):
    """Возвращает топ транзакции по сумме платежа"""
    sorted_by_spent = transactions_info.sort_values("Сумма платежа", ascending=True)

    top_transactions_list = []
    for index, row in sorted_by_spent.iterrows():
        top_transactions_list.append({
            "date": row["Дата платежа"],
            "amount": abs(row["Сумма платежа"]),
            "category": row["Категория"],
            "description": row["Описание"]
        })

    return top_transactions_list
