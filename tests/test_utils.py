import datetime
import json
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.utils import (
    filter_transactions_by_date_range,
    get_card_info,
    get_date_info,
    get_greeting,
    get_date_range,
    get_exchange_rates,
    get_stock_data,
    get_top_transactions,
    get_user_settings,
    read_excel_file,
)


@patch("pandas.read_excel")
def test_read_excel_file(mock_read):
    mock_read.return_value = {"Yes": 1, "No": 2}
    assert read_excel_file("transactions.xlsx") == {"Yes": 1, "No": 2}


def test_read_excel_file_incorrect_path():
    assert read_excel_file("incorrect_path").to_dict() == {}
    assert read_excel_file("operations.json").to_dict() == {}


@pytest.mark.parametrize(
    "date_info, expected",
    [
        ("2000-1-6 12:0:0", datetime.datetime(2000, 1, 6, 12, 0, 0)),
        ("2024-12-12 0:59:59", datetime.datetime(2024, 12, 12, 0, 59, 59)),
    ],
)
def test_get_date_info_correct_format(date_info, expected):
    assert get_date_info(date_info) == expected


@pytest.mark.parametrize("date_info, expected", [(datetime.datetime(2022, 1, 1, 5, 59, 59), "Доброй ночи"),
                                                 (datetime.datetime(2022, 1, 1, 6, 59, 59), "Доброе утро"),
                                                 (datetime.datetime(2022, 1, 1, 17, 59, 59), "Добрый день"),
                                                 (datetime.datetime(2022, 1, 1, 23, 59, 59), "Добрый вечер")])
@patch("src.utils.datetime")
def test_get_greeting(mock_datetime, date_info, expected):
    mock_datetime.now.return_value = date_info
    assert get_greeting() == expected


@pytest.mark.parametrize(
    "date_info, expected",
    [
        (datetime.datetime(2020, 1, 1), ["01.01.2020"]),
        (datetime.datetime(2012, 3, 3), ["01.03.2012", "02.03.2012", "03.03.2012"]),
    ],
)
def test_get_range_date(date_info, expected):
    assert get_date_range(date_info) == expected


def test_get_user_settings():
    mock_json = Mock(return_value={"cur": ["USD", "EUR"]})
    json.load = mock_json
    assert get_user_settings() == {"cur": ["USD", "EUR"]}


@patch("requests.get")
@patch("src.utils.get_user_settings")
def test_get_exchange_rates_status_code_200(mock_get_settings, mock_get):
    mock_get_settings.return_value = {"user_currencies": ["USD", "EUR"]}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"RUB": 1}}
    assert get_exchange_rates() == {"USD": 1, "EUR": 1}


@patch("requests.get")
@patch("src.utils.get_user_settings")
def test_get_exchange_rates_status_code_not_200(mock_get_settings, mock_get):
    mock_get_settings.return_value = {"user_currencies": ["USD", "EUR"]}
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"rates": {"RUB": 1}}
    assert get_exchange_rates() == {"USD": "No data", "EUR": "No data"}


@patch("requests.get")
@patch("src.utils.get_user_settings")
def test_get_stock_data_status_code_200(mock_get_settings, mock_get):
    mock_get_settings.return_value = {"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"price": 1}]
    assert get_stock_data() == {"AAPL": 1, "AMZN": 1, "GOOGL": 1, "MSFT": 1, "TSLA": 1}


@patch("requests.get")
@patch("src.utils.get_user_settings")
def test_get_stock_data_status_code_not_200(mock_get_settings, mock_get):
    mock_get_settings.return_value = {"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    mock_get.return_value.status_code = 100
    mock_get.return_value.json.return_value = [{"price": 1}]
    assert get_stock_data() == {
        "AAPL": "No data",
        "AMZN": "No data",
        "GOOGL": "No data",
        "MSFT": "No data",
        "TSLA": "No data",
    }


def test_filter_transactions_by_date_range(transactions_info_for_utils):
    res = filter_transactions_by_date_range(transactions_info_for_utils, ["01.01.2018", "02.01.2018"]).to_dict(
        "records")
    assert res == [{
        'Дата платежа': '02.01.2018', 'Номер карты': '*7198', 'Сумма платежа': -21.0, 'Категория': 'Красота',
        'Описание': 'OOO Balid'}]


def test_get_card_info(transactions_info_for_utils):
    assert get_card_info(transactions_info_for_utils) == [
        {"last_digits": "7197", "total_spent": 3800.0, "cashback": 38.0},
        {"last_digits": "7198", "total_spent": 21.0, "cashback": 0.21},
    ]


def test_get_top_transactions(transactions_info_for_utils):
    assert get_top_transactions(transactions_info_for_utils) == [
        {"date": "05.02.2018", "amount": 2500.0, "category": "Супермаркеты", "description": "Магнит"},
        {"date": "05.03.2018", "amount": 1300.0, "category": "Здоровье", "description": "Линзомат ТЦ Юность"},
        {"date": "02.01.2018", "amount": 21.0, "category": "Красота", "description": "OOO Balid"},
    ]
