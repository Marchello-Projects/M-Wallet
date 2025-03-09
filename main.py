from colorama import Fore, Style, init
from openpyxl import Workbook
from dotenv import load_dotenv
import requests
import os

init(autoreset=True)

exchange_rates = {}
user_wallets = []

def load_api_exchange_rate(currency: str):
    try:
        load_dotenv()
        api_key = os.getenv('API_KEY_EXCHANGE_RATE')
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/EUR'

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        for cur, rate in data['conversion_rates'].items():
            if cur == currency:
                exchange_rates.update({cur: rate})
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.HTTPError as e:
        print(e)

def load_api_bitcoin(vs_currencies: str) -> dict[str, dict[str, int]]:
    try: 
        vs_currencies = vs_currencies.lower()

        url_bitcoin = 'https://api.coingecko.com/api/v3/simple/price'

        params = {
            "ids": 'bitcoin',
            "vs_currencies": vs_currencies          
        }

        response = requests.get(url_bitcoin, params=params)
        response.raise_for_status()

        data = response.json()
        currencies_bitcoin = data['bitcoin'][vs_currencies]

        exchange_rates.update({'BTC': currencies_bitcoin})

        return data['bitcoin'][vs_currencies]
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.HTTPError as e:
        print(e)

def create_the_first_wallet(amount: str):
    amount = float(amount)

    user_wallets.append({
        'currency': 'EUR',
        'amount': amount   
    })

def create_a_wallet(currency: str, amount: str):
    currency = currency.upper()
    amount = float(amount)

    user_wallets.append({
        'currency': currency,
        'amount': amount   
    })

    load_api_exchange_rate(currency=currency)

username = input('Enter your username: ')
amount = input('Please, deposit your first money: ')

create_the_first_wallet(amount=amount)

while True:
    if not amount or not username:
        print('Empty string. Please, try again')
        break
    
    print('')
    print(rf'{Fore.GREEN}$$\      $$\         $$\      $$\           $$\ $$\            $$\     {Style.RESET_ALL}')
    print(rf'{Fore.GREEN}$$$\    $$$ |        $$ | $\  $$ |          $$ |$$ |           $$ |    {Style.RESET_ALL}')
    print(rf'{Fore.GREEN}$$$$\  $$$$ |        $$ |$$$\ $$ | $$$$$$\  $$ |$$ | $$$$$$\ $$$$$$\   {Style.RESET_ALL}')
    print(rf'{Fore.GREEN}$$\$$\$$ $$ |$$$$$$\ $$ $$ $$\$$ | \____$$\ $$ |$$ |$$  __$$\\_$$  _|  {Style.RESET_ALL}')
    print(rf'{Fore.GREEN}$$ \$$$  $$ |\______|$$$$  _$$$$ | $$$$$$$ |$$ |$$ |$$$$$$$$ | $$ |    {Style.RESET_ALL}')
    print(rf'{Fore.GREEN}$$ |\$  /$$ |        $$$  / \$$$ |$$  __$$ |$$ |$$ |$$   ____| $$ |$$\ {Style.RESET_ALL}')
    print(rf'{Fore.GREEN}$$ | \_/ $$ |        $$  /   \$$ |\$$$$$$$ |$$ |$$ |\$$$$$$$  \$$$$  | {Style.RESET_ALL}')
    print(rf'{Fore.GREEN}\__|     \__|        \__/     \__| \_______|\__|\__| \_______| \____/  {Style.RESET_ALL}')
    print(r'')
    print(r'')
    print(f'Hi {username}! The main currency in the program: EUR; Exchange rates: {exchange_rates}')
    print('Please, select the option:')
    print(f'1. Create a wallet\n2. Create a Bitcoin wallet\n3. Make a transfer to another wallet\n4. View all wallets\n5. Transaction history\n6. Delete all wallets\n7. Exit')

    option = input('Option: ')

    if option == '1':
        currency = input(f'Please, select a currency: ')
        amount = input('Please, deposit your first money: ')

        create_a_wallet(currency=currency, amount=amount)

    if option == '4':
        print('=' * 46)

        for index, wallet in enumerate(user_wallets):
            print(f'{index + 1}. {wallet}')

        print('=' * 46)
    
    if option == '7':
        break