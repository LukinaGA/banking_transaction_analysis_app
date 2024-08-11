import json
import os

from config import DATA_DIR, TRANSACTIONS
from src.utils import (
    filter_transactions_by_date_range,
    get_card_info,
    get_date_info,
    get_date_range,
    get_exchange_rates,
    get_greeting,
    get_stock_data,
    get_top_transactions,
    read_excel_file,
)

transactions_for_main = read_excel_file(TRANSACTIONS)
def get_main_page_info(date_info, transactions_info = transactions_for_main):
    """Записывает информацию для главной страницы в файл main_page.json"""
    date = get_date_info(date_info)

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
        "stock_prices": stock_data,
    }

    filename = os.path.join(DATA_DIR, "main_page.json")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(main_page, file, ensure_ascii=False, indent=4)
