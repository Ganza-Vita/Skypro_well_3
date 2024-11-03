def get_mask_card_number(card_number: str) -> str:
    """Функция маскирующая номер карты"""

    number_cards = ''.join(filter(str.isdigit, card_number))
    word = ''.join(filter(lambda x: not x.isdigit(), card_number)).strip()

    if len(number_cards) != 16:
        return "Номер карты должен содержать 16 цифр."
    masked_number = (
        f"{word} {number_cards[:4]} {number_cards[4:6]}** **** {number_cards[-4:]}"
    )
    return masked_number


def get_mask_account(account_number: str) -> str:
    """Функция, маскирующая номер счета"""
    account_number = account_number.strip()  # Убираем лишние пробелы

    # Отделяем текст и цифры
    words = account_number.split()
    word = ' '.join(filter(lambda x: not x.isdigit(), words))  # Текст, не содержащий цифр
    digits = ''.join(filter(str.isdigit, account_number))  # Все цифры в одну строку

    # Проверяем, что номер содержит хотя бы 4 цифры
    if len(digits) < 4:
        return "Номер счета должен содержать как минимум 4 цифры."

    # Маскируем номер, оставляя только последние 4 цифры
    masked_number = f"**{digits[-4:]}"

    # Формируем итоговый текст с замаскированным номером
    return f"{word}: {masked_number}"

f = get_mask_account('счет 6487346743687413')
print(f)
