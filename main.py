import json
import pandas as pd
from src.finance_operations import search_transactions, count_transaction_types


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
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
        transactions = pd.read_csv(file_path, delimiter=';').rename(columns=lambda x: x.strip().lower()).to_dict(orient='records')

    elif choice == "3":
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = pd.read_excel(file_path).to_dict(orient='records')
    else:
        print("Неверный выбор.")
        return

    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: ").strip().lower()
        if status in ['executed', 'canceled', 'pending']:
            print(f'Операции отфильтрованы по статусу "{status.upper()}"')
            filtered_transactions = [t for t in transactions if 'state' in t and isinstance(t['state'], str) and t['state'].lower() == status]

            if not filtered_transactions:
                print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
                return

            sort_choice = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
            if sort_choice == 'да':
                sort_order = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
                filtered_transactions.sort(key=lambda x: x['date'], reverse=(sort_order == 'по убыванию'))

            currency_filter = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
            if currency_filter == 'да':
                filtered_transactions = [t for t in filtered_transactions if t['currency_code'] == 'RUB']

            description_filter = input(
                "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ").strip().lower()
            if description_filter == 'да':
                query = input("Введите строку для поиска в описании: ")
                filtered_transactions = search_transactions(filtered_transactions, query)

            # Вывод результата
            print("Распечатываю итоговый список транзакций...")
            print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")

            for transaction in filtered_transactions:
                print(
                    f"{transaction['date']} {transaction['description']}\nСчет {transaction['from']}\nСумма: {transaction['amount']} {transaction['currency_code']}\n")
            break
        else:
            print(f'Статус операции "{status}" недоступен.')


if __name__ == "__main__":
    main()
