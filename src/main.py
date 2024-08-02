from src.utils import *
from datetime import datetime


def main():
    transactions_info = read_excel_file("..\\data\\operations.xlsx")

    try:
        date = datetime.strptime(input("Введите дату (ГГГГ ММ ДД ЧЧ ММ СС): "), "%Y %m %d %H %M %S")
    except Exception:
        date_default = (f"{transactions_info["Дата платежа"][0]} "
                        f"{datetime.now().hour}.{datetime.now().minute}.{datetime.now().second}")
        date = datetime.strptime(date_default, "%d.%m.%Y %H.%M.%S")
        print(f"Неверный формат даты, выбрана дата по умолчанию: {date}")

    date_range = get_date_range(date)

    filtered_transactions_by_date_range = filter_transactions_by_date_range(transactions_info, date_range)

    exchange_rates = []
    for currency, rate in get_exchange_rates().items():
        exchange_rates.append({"currency": currency, "rate": rate})

    stock_data = []
    for stock, price in get_stock_data().items():
        stock_data.append({"stock": stock, "price": price})

    main_page = {
        "greeting": greeting(date),
        "cards": get_card_info(filtered_transactions_by_date_range),
        "top_transactions": get_top_transactions(filtered_transactions_by_date_range)[:5],
        "currency_rates": exchange_rates,
        "stock_prices": stock_data
    }

    return main_page
