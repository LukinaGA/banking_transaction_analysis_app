import re
from src.utils import read_excel_file


def simple_search(transactions_info, search_word):
    """Возвращает список транзакций с заданным описанием"""
    found_transactions = []
    # print(transactions_info.to_dict(orient="records"))
    for transaction in transactions_info.to_dict(orient="records"):
        if re.search(search_word, transaction.get("Описание"), flags=re.IGNORECASE):
            found_transactions.append(transaction)

        if re.search(search_word, str(transaction.get("Категория")), flags=re.IGNORECASE):
            found_transactions.append(transaction)

    return found_transactions


if __name__ == '__main__':
    simple_search(read_excel_file("..\\data\\operations.xlsx"), "перевод")
