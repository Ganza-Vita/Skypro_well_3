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

    transactions = []
    try:
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
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return

    data_exists = False  # Флаг для проверки наличия данных
    for t in transactions:
        from_value = t.get('from')
        if pd.isna(from_value):
            t['masked_from'] = "Данные отсутствуют."
            continue
        elif isinstance(from_value, str):
            digits = ''.join(filter(str.isdigit, from_value))
            if len(digits) == 16:
                t['masked_from'] = get_mask_card_number(digits)
            elif len(digits) >= 4:
                t['masked_from'] = get_mask_account(digits)
            else:
                t['masked_from'] = from_value
            data_exists = True
        else:
            t['masked_from'] = "Неизвестный формат данных."

    if not data_exists:
        print("Данные отсутствуют.")
        return

    while True:
        # Фильтрация по статусу
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
        ).strip().lower()

        if status in ['executed', 'canceled', 'pending']:
            print(f'Операции отфильтрованы по статусу "{status.upper()}"')
            filtered_transactions = [
                t for t in transactions if 'state' in t and isinstance(t['state'], str) and t['state'].lower() == status
            ]
            break
        else:
            print(f'Статус "{status}" недоступен.\nПожалуйста, введите корректный статус.')

    while True:
        # Фильтрация по дате
        date_filter = input("Хотите отфильтровать по дате? (да/нет): ").strip().lower()
        if date_filter == "да":
            start_date = input("Введите начальную дату (ДД.ММ.ГГГГ): ")
            end_date = input("Введите конечную дату (ДД.ММ.ГГГГ): ")

            filtered_transactions = [
                t for t in filtered_transactions
                if start_date <= format_date(t['date']) <= end_date
            ]
            break
        elif date_filter == "нет":
            break

    # Сортировка
    while True:
        sort_order = input("Хотите отсортировать по дате? (по возрастанию/по убыванию/нет): ").strip().lower()
        if sort_order == "по возрастанию":
            filtered_transactions.sort(key=lambda x: x['date'])
            break
        elif sort_order == "по убыванию":
            filtered_transactions.sort(key=lambda x: x['date'], reverse=True)
            break
        elif sort_order == "нет":
            break

    # Фильтрация по рублевым транзакциям
    while True:
        rub_filter = input("Хотите отфильтровать рублевые транзакции? (да/нет): ").strip().lower()
        if rub_filter == "да":
            filtered_transactions = [
                t for t in filtered_transactions if t.get('currency_code') == 'RUB'
            ]
            break
        elif rub_filter == "нет":
            break

    # Фильтрация по слову в описании
    while True:
        word_filter = input("Хотите отфильтровать по слову в описании? (да/нет): ").strip().lower()
        if word_filter == "да":
            word = input("Введите слово для фильтрации: ")
            filtered_transactions = [
                t for t in filtered_transactions if word.lower() in t.get('description', '').lower()
            ]
            break
        elif word_filter == "нет":
            break

    # Вывод отфильтрованных и отсортированных транзакций
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, соответствующей критериям.")
    else:
        for transaction in filtered_transactions:
            print(f"{format_date(transaction['date'])} - {transaction['description']}")
            print(f"Счет: {transaction.get('masked_from', 'Данные отсутствуют.')}")
            print(f"Сумма: {transaction['amount']} {transaction['currency_code']}\n")


if __name__ == "__main__":
    main()