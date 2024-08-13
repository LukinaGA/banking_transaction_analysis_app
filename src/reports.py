import datetime
import logging
import os

import pandas as pd

from config import DATA_DIR, ROOT_DIR, TRANSACTIONS
from src.utils import read_excel_file

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
    filename=os.path.join(ROOT_DIR, "logs", "logs.log"),
    encoding="utf-8",
    filemode="w",
)
logger = logging.getLogger("reports")


def send_to_file(filename="spending_by_category.xlsx"):
    """Записывает полученный отчет в XLSX-файл с заданным именем"""

    def inner(func):
        def wrapper(*args, **kwargs):
            data = pd.DataFrame(func(*args, **kwargs))
            file_path = os.path.join(DATA_DIR, filename)
            logger.debug(f"Запись отчета в файл {filename}")
            data.to_excel(file_path)

        return wrapper

    return inner


@send_to_file()
def spending_by_category(category, date=datetime.datetime.now(), transactions_info=read_excel_file(TRANSACTIONS)):
    """Возвращает отчет о расходах за 3 месяца по заданной категории"""
    logger.info("Запуск функции spending_by_category()")
    logger.debug("Получение диапозона дат за 3 месяца")

    start_date = date - datetime.timedelta(days=90)
    date_range = pd.date_range(min(start_date, date), max(start_date, date)).strftime("%d.%m.%Y").tolist()

    logger.debug(f"Поиск расходов по категории '{category}'")
    filtered_transactions: pd.DataFrame = transactions_info.loc[
        transactions_info["Дата платежа"].isin(date_range)
        & (transactions_info["Категория"] == category)
        & (transactions_info["Сумма платежа"] < 0)
    ]

    result = [{category: filtered_transactions["Сумма платежа"].sum()}]

    return result
