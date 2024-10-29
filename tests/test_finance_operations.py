from unittest.mock import mock_open, patch

import pytest

from src.finance_operations import read_financial_operations_from_csv, read_financial_operations_from_excel


# Тестирование для CSV
def test_read_financial_operations_from_csv():
    mock_data = (
        "id,state,date,amount,currency_name,currency_code,from,to,description\n"
        "650703,EXECUTED,2023-09-05T11:30:32Z,16210,Sol,PEN,Счет 58803664561298323391,Счет 39745660563456619397,Перевод организации\n"
    )

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = read_financial_operations_from_csv("dummy_path.csv")

    expected = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]

    assert result == expected


# Тестирование для Excel
def test_read_financial_operations_from_excel():
    mock_data = {
        "id": [650703],
        "state": ["EXECUTED"],
        "date": ["2023-09-05T11:30:32Z"],
        "amount": [16210],
        "currency_name": ["Sol"],
        "currency_code": ["PEN"],
        "from": ["Счет 58803664561298323391"],
        "to": ["Счет 39745660563456619397"],
        "description": ["Перевод организации"],
    }

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value.to_dict.return_value = mock_data
        result = read_financial_operations_from_excel("dummy_path.xlsx")

    expected = [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]

    assert result == expected
