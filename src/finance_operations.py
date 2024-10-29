import csv
from typing import Dict, List

import pandas as pd

file_path_csv = "C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\src\\transactions.csv"
file_path_excel = "C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\src\\transactions_excel.xlsx"


def read_financial_operations_from_csv(file_path_csv: str) -> List[Dict]:
    """
    Считывает финансовые операции из CSV-файла.

    :param file_path: Путь к CSV-файлу.
    :return: Список словарей с транзакциями.
    """
    transactions = []
    with open(file_path_csv, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            transactions.append(row)
    return transactions


def read_financial_operations_from_excel(file_path_excel: str) -> List[Dict]:
    """
    Считывает финансовые операции из Excel-файла.

    :param file_path: Путь к Excel-файлу.
    :return: Список словарей с транзакциями.
    """
    df = pd.read_excel(file_path_excel)
    return df.to_dict(orient="records")
