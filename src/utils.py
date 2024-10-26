import json

from external_api import converts_currency


def returns_a_list_of_transactions(file_path: str) -> list:
    """ Функция возвращает список словарей с транзакиями из JSON-файла """
    try:
        with open(file_path, 'r', encoding='utf-8') as file_transaction:
            return json.load(file_transaction)
    except (FileNotFoundError, UnicodeDecodeError) as e:
        return []


def returns_the_transaction_amount(transactions: list) -> float:
    """ Функция возвращает суммы транзакций """
    if not transactions:
        return 0.0

    total_amount = 0.0

    for transaction in transactions:
        if transaction.get("operationAmount") and transaction["operationAmount"]["currency"]["code"] == "RUB":
            total_amount += float(transaction["operationAmount"]["amount"])
        elif transaction.get("operationAmount"):
            currency_code = transaction["operationAmount"]["currency"]["code"]
            amount = transaction["operationAmount"]["amount"]
            total_amount += converts_currency("RUB", currency_code, float(amount))

    return total_amount



file_path = 'C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\data\\operations.json'
transactions = returns_a_list_of_transactions(file_path)

total_in_rub = returns_the_transaction_amount(transactions)

print(f"Общая сумма транзакций в рублях: {total_in_rub}")
