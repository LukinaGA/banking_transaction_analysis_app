import json
import logging
import os
import re

from config import DATA_DIR, ROOT_DIR, TRANSACTIONS
from src.utils import read_excel_file

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
    filename=os.path.join(ROOT_DIR, "logs", "logs.log"),
    encoding="utf-8",
    filemode="w",
)
logger = logging.getLogger("services")

transactions = read_excel_file(TRANSACTIONS)
def simple_search(search_word, transactions_info=transactions):
    """Записывает список транзакций с заданным описанием в файл simple_search.json"""
    logger.info("Запуск функции simple_search()")

    found_transactions = []
    logger.debug(f"Поиск в описании и категориях слова '{search_word}'")
    for transaction in transactions_info.to_dict(orient="records"):
        if re.search(search_word, transaction.get("Описание"), flags=re.IGNORECASE):
            found_transactions.append(transaction)

        if re.search(search_word, str(transaction.get("Категория")), flags=re.IGNORECASE):
            found_transactions.append(transaction)

    logger.info("Запись результата в файл services.json")
    filename = os.path.join(DATA_DIR, "simple_search.json")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(found_transactions, file, ensure_ascii=False, indent=4)
