from src.utils import *

transactions_info = read_excel_file("..\\data\\operations.xlsx")

date = get_user_date()

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

print(json.dumps(main_page, indent=2, ensure_ascii=False))
