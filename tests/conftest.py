import pandas as pd
import pytest


@pytest.fixture
def transactions_info_for_utils():
    transactions = {
        "Дата платежа": ["02.01.2018", "05.02.2018", "05.03.2018"],
        "Номер карты": ["*7198", "*7197", "*7197"],
        "Сумма платежа": [21.0, -2500.0, -1300.0],
        "Категория": ["Красота", "Супермаркеты", "Здоровье"],
        "Описание": ["OOO Balid", "Магнит", "Линзомат ТЦ Юность"],
    }

    return pd.DataFrame(transactions)


@pytest.fixture
def transactions_info_for_services():
    transactions = {
        "Дата платежа": ["31.12.2021", "31.12.2021", "24.12.2021"],
        "Номер карты": ["*1555", "*1234", "*1324"],
        "Сумма платежа": [-800.0, -20000.0, -2000.0],
        "Категория": ["Красота", "Переводы", "Категория"],
        "Описание": ["OOO Balid", "Константин Л.", "Переводы на карту"],
    }

    return pd.DataFrame(transactions)


@pytest.fixture
def transactions_info_for_reports():
    transactions = {
        "Дата платежа": ["31.12.2021", "31.12.2021", "24.12.2021"],
        "Сумма платежа": [-800.0, -20000.0, -2000.0],
        "Категория": ["Красота", "Красота", "Категория"],
    }

    return pd.DataFrame(transactions)
