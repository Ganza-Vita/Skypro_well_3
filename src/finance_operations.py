import csv
from typing import Dict, List

import pandas as pd

import re
from collections import Counter

file_path_csv = "C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\data\\transactions.csv"
file_path_excel = "C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\data\\transactions_excel.xlsx"


def read_financial_operations_from_csv(file_path_csv: str) -> List[Dict]:
    """    Считывает финансовые операции из CSV-файла.    """
    transactions = []
    with open(file_path_csv, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            transactions.append(row)
    return transactions


def read_financial_operations_from_excel(file_path_excel: str) -> List[Dict]:
    """    Считывает финансовые операции из Excel-файла.    """
    df = pd.read_excel(file_path_excel)
    return df.to_dict(orient="records")


def search_transactions(transactions: List[Dict], query: str) -> List[Dict]:
    """    Ищет транзакции по описанию.    """
    pattern = re.compile(re.escape(query), re.IGNORECASE)  # Регистронезависимый поиск
    return [transaction for transaction in transactions if pattern.search(transaction.get('description', ''))]

def count_transaction_types(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """    Подсчитывает количество операций определенных типов.    """
    category_count = Counter()
    for transaction in transactions:
        description = transaction.get('description')
        if description in categories:
            category_count[description] += 1
    return dict(category_count)
