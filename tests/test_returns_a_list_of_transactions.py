from unittest import mock, main
from src.external_api import converts_currency
from src.utils import (returns_a_list_of_transactions, returns_the_transaction_amount)

# Тест для функции returns_a_list_of_transactions
@mock.patch("builtins.open", new_callable=mock.mock_open, read_data='[{"operationAmount": {"currency": {"code": "RUB"}, "amount": "1500"}},{"operationAmount": {"currency": {"code": "USD"}, "amount": "100"}}]')
def test_returns_a_list_of_transactions_success(mock_file):
    result = returns_a_list_of_transactions("mock_path.json")
    expected = [
        {"operationAmount": {"currency": {"code": "RUB"}, "amount": "1500"}},
        {"operationAmount": {"currency": {"code": "USD"}, "amount": "100"}}
    ]
    assert result == expected

# Тест на случай, если файл не найден
@mock.patch("builtins.open", side_effect=FileNotFoundError)
def test_returns_a_list_of_transactions_file_not_found(mock_file):
    result = returns_a_list_of_transactions("mock_path.json")
    assert result == []

# Тест на случай ошибки декодирования JSON
@mock.patch("builtins.open", new_callable=mock.mock_open, read_data='invalid json')
def test_returns_a_list_of_transactions_json_decode_error(mock_file):
    result = returns_a_list_of_transactions("mock_path.json")
    assert result == []

# Тест для функции returns_the_transaction_amount
@mock.patch('external_api.converts_currency', return_value=200.0)
def test_returns_the_transaction_amount(mock_converts_currency):
    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}, "amount": "1500"}},
        {"operationAmount": {"currency": {"code": "USD"}, "amount": "100"}},
        {"operationAmount": {"currency": {"code": "EUR"}, "amount": "50"}},
    ]
    total = returns_the_transaction_amount(transactions)
    assert total == 1500 + 200.0 + 200.0  # 200.0 - результат конвертации

# Тест на пустой список транзакций
def test_returns_the_transaction_amount_empty_list():
    result = returns_the_transaction_amount([])
    assert result == 0.0

# Тест на отсутствие данных в транзакциях
def test_returns_the_transaction_amount_with_missing_data():
    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}, "amount": "1500"}},
        {"operationAmount": {"currency": {"code": "USD"}}},  # Пропущено поле amount
        {"operationAmount": None},  # None вместо словаря
    ]
    total = returns_the_transaction_amount(transactions)
    assert total == 1500.0

if __name__ == "__main__":
    main()
