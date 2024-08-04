import re
from src.utils import read_excel_file
from config import TRANSACTIONS

def simple_search(transactions_info, search_word):
    """Возвращает список транзакций с заданным описанием"""
    found_transactions = []
    for transaction in transactions_info.to_dict(orient="records"):
        if re.search(search_word, transaction.get("Описание"), flags=re.IGNORECASE):
            found_transactions.append(transaction)

        if re.search(search_word, str(transaction.get("Категория")), flags=re.IGNORECASE):
            found_transactions.append(transaction)

    return found_transactions


if __name__ == '__main__':
    print(simple_search(read_excel_file(TRANSACTIONS), "перевод"))
