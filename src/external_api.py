import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("external_api")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs\\external_api.log", "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def converts_currency(dict_transactions) -> float:
    """Функция конвертирует валютую по текущему курсу валют"""
    logging.info(f"Получение API ключа")
    apilayer_token = os.getenv("API_KEY_APILAYER")

    if not apilayer_token:
        logging.error(f"API ключ не найден")
        print("API ключ не найден. Убедитесь, что он сохранён в .env файле.")
        return 0.0

    url = "https://api.apilayer.com/exchangerates_data/convert"

    params = dict_transactions

    headers = {"apikey": f"{apilayer_token}"}

    logging.info(f"GET-запрос на APIlayer")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        logging.info(f"Статус - Ок")
        content = response.json()
        return content["result"]
    else:
        logging.error(f"Ошибка API: {response.status_code} - {response.text}")
        return 0.0
