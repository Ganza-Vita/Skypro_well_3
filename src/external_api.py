import os
from dotenv import load_dotenv
import requests

load_dotenv()

def converts_currency(to: str, fro: str, amount: float) -> float:
    apilayer_token = os.getenv('API_KEY_APILAYER')

    if not apilayer_token:
        print("API ключ не найден. Убедитесь, что он сохранён в .env файле.")
        return 0.0

    url = 'https://api.apilayer.com/exchangerates_data/convert'

    params = {
        'to': to,
        'from': fro,
        'amount': amount
    }

    headers = {
        'Authorization': f'apikey {apilayer_token}'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        content = response.json()
        return content['result']
    else:
        print(f"Ошибка API: {response.status_code} - {response.text}")
        return 0.0