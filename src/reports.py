import json
import datetime
import pandas as pd


def write_to_file(func):
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        with open("..\\data\\report.json", "a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    return wrapper

@write_to_file
def spending_by_category(transactions_info, category, date=datetime.datetime.now()):
    start_date = date - datetime.timedelta(days=90)
    date_range = pd.date_range(min(start_date, date), max(start_date, date)).strftime('%d.%m.%Y').tolist()

    filtered_transactions: pd.DataFrame = transactions_info.loc[
        transactions_info["Дата платежа"].isin(date_range) & (transactions_info["Категория"] == category) & (
                    transactions_info["Сумма платежа"] < 0)]

    result = {category: filtered_transactions["Сумма платежа"].sum()}

    return result
