import pandas as pd
import os
import json

from src.services import simple_search
from config import DATA_DIR


def test_simple_search(transactions_info_for_services):
    simple_search("перевод", transactions_info=transactions_info_for_services)
    with open(os.path.join(DATA_DIR, "simple_search.json"), encoding="utf-8") as file:
        data = json.load(file)
    assert data == [
        {
            "Дата платежа": "31.12.2021",
            "Номер карты": "*1234",
            "Сумма платежа": -20000.0,
            "Категория": "Переводы",
            "Описание": "Константин Л.",
        },
        {
            "Дата платежа": "24.12.2021",
            "Номер карты": "*1324",
            "Сумма платежа": -2000.0,
            "Категория": "Категория",
            "Описание": "Переводы на карту",
        },
    ]


def test_simple_search_not_found(transactions_info_for_services):
    simple_search("поиск", transactions_info=transactions_info_for_services)
    with open(os.path.join(DATA_DIR, "simple_search.json"), encoding="utf-8") as file:
        data = json.load(file)
    assert data == []


def test_simple_search_empty_data():
    simple_search("перевод", transactions_info=pd.DataFrame())
    with open(os.path.join(DATA_DIR, "simple_search.json"), encoding="utf-8") as file:
        data = json.load(file)
    assert data == []
