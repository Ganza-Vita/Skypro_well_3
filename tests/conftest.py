import pytest


@pytest.fixture()
def return_list_transactions_1() -> list:
    return 'C:\\Users\\Bulat\\PycharmProjects\\Skypro_well_3\\data\\opesarations.json'


@pytest.fixture()
def return_list_transactions_2() -> list:
    return []