from colorama import Fore, Style, init
from openpyxl import Workbook
from dotenv import load_dotenv
import requests
import os

init(autoreset=True)

exchange_rates = {}
user_wallets = []

def load_api_exchange_rate(currency: str, select_currency: str):
    try:
        currency = currency.upper()
        select_currency = select_currency.upper()

        load_dotenv()
        api_key = os.getenv('API_KEY_EXCHANGE_RATE')
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}'

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        for cur, rate in data['conversion_rates'].items():
            if cur != select_currency:
                continue
            else:
                exchange_rates.update({cur: rate})
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.HTTPError as e:
        print(e)

