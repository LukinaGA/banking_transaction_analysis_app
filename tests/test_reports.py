import os
from datetime import datetime

import pandas as pd

from config import DATA_DIR
from src.reports import send_to_file, spending_by_category


def test_send_to_file():
    @send_to_file("test.xlsx")
    def some_function():
        return pd.DataFrame([{"Yes": [50, 21], "No": [131, 2]}])

    some_function()

    assert pd.read_excel(os.path.join(DATA_DIR, "test.xlsx"), index_col=0).to_dict(orient="records") == [
        {"Yes": "[50, 21]", "No": "[131, 2]"}
    ]


def test_spending_by_category(transactions_info_for_reports):
    spending_by_category("Красота", date=datetime(2022, 2, 1), transactions_info=transactions_info_for_reports)
    res = pd.read_excel(os.path.join(DATA_DIR, "spending_by_category.xlsx"), index_col=0).to_dict(orient="records")
    expected = [{"Красота": -20800.0}]
    assert res == expected


def test_spending_by_category_no_date(transactions_info_for_reports):
    spending_by_category("Красота", transactions_info=transactions_info_for_reports)
    res = pd.read_excel(os.path.join(DATA_DIR, "spending_by_category.xlsx"), index_col=0).to_dict(orient="records")
    expected = [{"Красота": 0}]
    assert res == expected


def test_spending_by_category_no_valid_category(transactions_info_for_reports):
    spending_by_category("Госуслуги", transactions_info=transactions_info_for_reports)
    res = pd.read_excel(os.path.join(DATA_DIR, "spending_by_category.xlsx"), index_col=0).to_dict(orient="records")
    expected = [{"Госуслуги": 0}]
    assert res == expected
