import pandas as pd
import pytest


@pytest.fixture
def transactions_info_for_test():
    transactions = {'Дата платежа': ['02.01.2018', '05.02.2018', '05.03.2018'],'Номер карты': ['*7198', '*7197', '*7197'], 'Сумма платежа': [21.0, -2500.0, -1300.0], 'Категория': ['Красота', 'Супермаркеты', 'Здоровье'],
         'Описание': ['OOO Balid', 'Магнит', 'Линзомат ТЦ Юность']}

    return pd.DataFrame(transactions)
