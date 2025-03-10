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
    if not amount:
        print('Empty string. Please, try again')
        return
    
    amount = float(amount)

    user_wallets.append({
        'currency': 'EUR',
        'amount': amount   
    })

def create_a_wallet(currency: str, amount: str):
    if not currency or not amount:
        print('Empty string. Please, try again')
        return
    
    currency = currency.upper()
    amount = float(amount)

    user_wallets.append({
        'currency': currency,
        'amount': amount   
    })

    load_api_exchange_rate(currency=currency)

def create_a_bitcoin_wallet(select_wallet: str, amount: str):
    if select_wallet == 'BTC':
        print('Unable to use bitcoin wallet')
        return
    
    if not amount or not select_wallet:
        print('Empty string. Please, try again')
        return
    
    select_wallet = select_wallet.upper()
    amount = float(amount)

    for wallet in user_wallets:
        if wallet.get('currency') == select_wallet:
            get_price_BTC = load_api_bitcoin(vs_currencies=select_wallet.lower())

            if get_price_BTC is None:
                print(f"Failed to fetch Bitcoin price for {select_wallet}. Try again later.")
                return

            if wallet['amount'] < amount:
                print(f"Not enough funds in {select_wallet} wallet.")
                return
            
            BTC_amount = amount / get_price_BTC

            wallet['amount'] -= amount

            user_wallets.append({
                'currency': 'BTC',
                'amount': BTC_amount
            })

username = input('Enter your username: ')
amount = input('Please, deposit your first money: ')

create_the_first_wallet(amount=amount)

while True:
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
    print(f'Hi {username}! The main currency in the program: EUR')
    print('Please, select the option:')
    print(f'1. Create a wallet\n2. Create a Bitcoin wallet\n3. Make a transfer to another wallet\n4. View all wallets\n5. View all exchange rates\n6. Transaction history\n7. Delete all wallets\n8. Exit')

    option = input('Option: ')

    if option == '1':
        currency = input(f'Please, select a currency: ')
        amount = input('Please, deposit your first money: ')

        create_a_wallet(currency=currency, amount=amount)

    if option == '2':
        print('=' * 46)

        for index, wallet in enumerate(user_wallets):
                    print(f'{index + 1}. {wallet}')

        print('=' * 46)

        select_wallet = input('Please, select your wallet: ')
        amount_from_card = input('Please, enter enter the amount: ')

        create_a_bitcoin_wallet(select_wallet=select_wallet, amount=amount_from_card)

    if option == '4':
        print('=' * 46)

        for index, wallet in enumerate(user_wallets):
            print(f'{index + 1}. {wallet}')

        print('=' * 46)

    if option == '5':
        print('=' * 46)

        for currency, item in exchange_rates.items():
            print(f'{currency}: {item}')

        print('=' * 46)
    
    if option == '8':
        break