from unittest.mock import Mock, patch

from src.utils import returns_a_list_of_transactions


def test_returns_a_list_of_transactions(return_list_transactions_1):
    assert returns_a_list_of_transactions(return_list_transactions_1) == []


def test_returns_a_list_of_transactions(return_list_transactions_2):
    assert returns_a_list_of_transactions(return_list_transactions_2) == []
