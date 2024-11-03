import json
import pandas as pd
from src.masks import get_mask_card_number, get_mask_account


def format_date(date_string):
    """Форматирует дату в формат DD.MM.YYYY."""
    if pd.notna(date_string):  # Проверяем, что значение не NaN
        return pd.to_datetime(date_string).strftime('%d.%m.%Y')
    return date_string


def main():
    print("Привет!\nДобро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    choice = input("Пользователь: ")
    if choice == "1":
        file_path = input("Введите путь к JSON-файлу: ")
        with open(file_path) as f:
            transactions = json.load(f)
    elif choice == "2":
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = pd.read_csv(file_path, delimiter=';').rename(columns=lambda x: x.strip().lower()).to_dict(
            orient='records')
    elif choice == "3":
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = pd.read_excel(file_path).to_dict(orient='records')
    else:
        print("Неверный выбор.")
        return
    data_exists = False  # Флаг для проверки наличия данных
    for t in transactions:
        from_value = t.get('from')  # Получаем значение по ключу 'from'
        if pd.isna(from_value):  # Проверка на NaN
            t['masked_from'] = "Данные отсутствуют."
            continue
        elif isinstance(from_value, str):  # Проверяем, что значение является строкой
            digits = ''.join(filter(str.isdigit, from_value))  # Извлекаем только цифры
            if len(digits) == 16:  # Если это 16 цифр
                t['masked_from'] = get_mask_card_number(digits)
            elif len(digits) >= 4:  # Если это больше или равно 4 цифрам, но не 16
                t['masked_from'] = get_mask_account(digits)
            else:
                t['masked_from'] = from_value  # Если цифр меньше 4, оставляем как есть
            data_exists = True  # Обновляем флаг, что данные найдены
        else:
            t['masked_from'] = "Неизвестный формат данных."
    if not data_exists:  # Если данных не было найдено
        print("Данные отсутствуют.")
        return
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
        ).strip().lower()
        if status in ['executed', 'canceled', 'pending']:
            print(f'Операции отфильтрованы по статусу "{status.upper()}"')
            filtered_transactions = [
                t for t in transactions if 'state' in t and isinstance(t['state'], str) and t['state'].lower() == status
            ]
            # Проверка на наличие отфильтрованных транзакций
            if not filtered_transactions:
                print("Не найдено ни одной транзакции, соответствующей критериям.")
            else:
                for transaction in filtered_transactions:
                    print(f"{format_date(transaction['date'])} - {transaction['description']}")
                    # Используем 'masked_from', так как теперь он определен для каждой транзакции.
                    print(f"Счет: {transaction.get('masked_from', 'Данные отсутствуют.')}")
                    print(f"Сумма: {transaction['amount']} {transaction['currency_code']}\n")
            break
        else:
            print(f'Статус "{status}" недоступен.\nПожалуйста, введите корректный статус.')


if __name__ == "__main__":
    main()
