from src.services import simple_search
import pandas as pd


def test_simple_search(transactions_info_for_services):
    assert simple_search(transactions_info_for_services, "перевод") == [
        {'Дата платежа': '31.12.2021', 'Номер карты': "*1234", 'Сумма платежа': -20000.0, 'Категория': 'Переводы',
         'Описание': 'Константин Л.'},
        {'Дата платежа': '24.12.2021', 'Номер карты': "*1324", 'Сумма платежа': -2000.0, 'Категория': 'Категория',
         'Описание': 'Переводы на карту'}]

def test_simple_search_not_found(transactions_info_for_services):
    assert simple_search(transactions_info_for_services, "поиск") == []


def test_simple_search_empty():
    assert simple_search(pd.DataFrame(), "перевод") == []

