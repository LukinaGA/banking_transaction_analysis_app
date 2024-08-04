import json

from src.utils import *
from config import TRANSACTIONS


def get_main_page_info(date_info):
    """Возвращает информацию для главной страницы"""
    date = get_date_info(date_info)

    transactions_info = read_excel_file(TRANSACTIONS)

    date_range = get_date_range(date)

    filtered_transactions_by_date_range = filter_transactions_by_date_range(transactions_info, date_range)

    exchange_rates = []
    for currency, rate in get_exchange_rates().items():
        exchange_rates.append({"currency": currency, "rate": rate})

    stock_data = []
    for stock, price in get_stock_data().items():
        stock_data.append({"stock": stock, "price": price})

    main_page = {
        "greeting": get_greeting(),
        "cards": get_card_info(filtered_transactions_by_date_range),
        "top_transactions": get_top_transactions(filtered_transactions_by_date_range)[:5],
        "currency_rates": exchange_rates,
        "stock_prices": stock_data
    }

    return main_page
