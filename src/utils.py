import json



def returns_a_list_of_transactions(file_path: str) -> list:
    """ Функция возвращает список словарей с транзакиями из JSON-файла """
    try:
        with open(file_path, 'r', encoding='utf-8') as file_transaction:
            return file_transaction.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        return []




file_path = 'C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\data\\operatins.json'
file_content = returns_a_list_of_transactions(file_path)
print(file_content)