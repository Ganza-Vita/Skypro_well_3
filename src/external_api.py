import os
from dotenv import load_dotenv
import requests

load_dotenv()

def converts_currency(dict_transactions) -> float:
    """ Функция конвертирует валютую по текущему курсу валют """

    apilayer_token = os.getenv('API_KEY_APILAYER')

    if not apilayer_token:
        print("API ключ не найден. Убедитесь, что он сохранён в .env файле.")
        return 0.0

    url = 'https://api.apilayer.com/exchangerates_data/convert'

    params = dict_transactions

    headers = {
        "apikey": f"{apilayer_token}"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        content = response.json()
        return content['result']
    else:
        print(f"Ошибка API: {response.status_code} - {response.text}")
        return 0.0