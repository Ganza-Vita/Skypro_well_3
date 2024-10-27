import json
import logging

from src.external_api import converts_currency


logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs\\utils.log", 'w', encoding='UTF-8')
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def returns_a_list_of_transactions(file_path: str) -> list:
    """Функция возвращает список словарей с транзакиями из JSON-файла"""
    try:
        logging.info(f"Возврат списка словарей из JSON-файла")
        if file_path != []:
            with open(file_path, "r", encoding="utf-8") as file_transaction:
                return json.load(file_transaction)
        else:
            return []
    except (FileNotFoundError, UnicodeDecodeError) as e:
        logging.error(f"Произошла ошибка возврата словарей")
        return []


def returns_the_transaction_amount(transactions: list) -> float:
    """Функция возвращает суммы транзакций"""
    logging.info(f"Проверка наличия транзакции")
    if not transactions:
        return 0.0

    total_amount = 0.0

    for transaction in transactions:
        logging.info(f"Возврат суммы транзакций, если валюта транзакции 'RUB'")
        if transaction.get("operationAmount") and transaction["operationAmount"]["currency"]["code"] == "RUB":
            total_amount += float(transaction["operationAmount"]["amount"])
        elif transaction.get("operationAmount"):
            logging.info(
                f"Возврат суммы транзакций, если валюта транзакции не 'RUB'")
            dict_transaction = {}
            currency_code = transaction["operationAmount"]["currency"]["code"]
            amount = transaction["operationAmount"]["amount"]
            dict_transaction["to"] = "RUB"
            dict_transaction["from"] = currency_code
            dict_transaction["amount"] = amount
            logging.info(f"Передача суммы транзакции для конвертации")
            total_amount += converts_currency(dict_transaction)

    return total_amount


file_path = "C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\data\\operations.json"
transactions = returns_a_list_of_transactions(file_path)

total_in_rub = returns_the_transaction_amount(transactions)

print(f"Общая сумма транзакций в рублях: {total_in_rub}")
