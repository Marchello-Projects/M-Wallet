from colorama import Fore, Style, init
from openpyxl import Workbook
from dotenv import load_dotenv
import requests
import os

init(autoreset=True)
workbook_transaction = Workbook()

exchange_rates = {}
user_wallets = []
transactions = []

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
    print(f'Wallet created: {user_wallets}')
    transactions.append(f'Wallet created: {user_wallets}')

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

            print(f'Bitcoin wallet created: {user_wallets}')
            transactions.append(f'Bitcoin wallet created: {user_wallets}')

def make_a_transfer(select_first_wallet: str, select_second_wallet: str, amount: str):
    if len(user_wallets) == 1:
        print('You only have one wallet.')
        return
    
    if not select_first_wallet or not select_second_wallet or not amount:
        print('Empty string. Please, try again')
        return
    
    select_first_wallet = select_first_wallet.upper()
    select_second_wallet = select_second_wallet.upper()
    amount = float(amount)
    
    first_wallet = None
    second_wallet = None
    
    for wallet in user_wallets:
        if wallet['currency'] == select_first_wallet:
            first_wallet = wallet
        if wallet['currency'] == select_second_wallet:
            second_wallet = wallet
    
    if first_wallet is None or second_wallet is None:
        print('One or both wallets do not exist.')
        return
    
    if first_wallet['amount'] < amount:
        print(f'Not enough funds in {select_first_wallet} wallet.')
        return
    
    if select_first_wallet == select_second_wallet:
        print('Cannot transfer to the same wallet.')
        return
    
    if select_first_wallet not in exchange_rates:
        load_api_exchange_rate(select_first_wallet)
    if select_second_wallet not in exchange_rates:
        load_api_exchange_rate(select_second_wallet)
    
    if select_first_wallet not in exchange_rates or select_second_wallet not in exchange_rates:
        print(f'Exchange rate for {select_first_wallet} or {select_second_wallet} is not available.')
        return
    
    rate_from = exchange_rates.get(select_first_wallet, 1)
    rate_to = exchange_rates.get(select_second_wallet, 1)
    converted_amount = amount * (rate_to / rate_from)
    
    first_wallet['amount'] -= amount
    second_wallet['amount'] += converted_amount
    
    print(f'Successfully transferred {amount} {select_first_wallet} to {converted_amount:.2f} {select_second_wallet}')
    transactions.append(f'Successfully transferred {amount} {select_first_wallet} to {converted_amount:.2f} {select_second_wallet}.')

username = input('Enter your username: ')
first_amount = input('Please, deposit your first money: ')

if username != '' or first_amount != '':
    create_the_first_wallet(amount=first_amount)

    print(f'The first wallet has been created: {user_wallets}')
    transactions.append(f'The first wallet has been created: {user_wallets}')

while True:
    if not username or not first_amount:
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
    print(f'Hi {username}! The main currency in the program: EUR')
    print('Please, select the option:')
    print(f'1. Create a wallet\n2. Create a Bitcoin wallet\n3. Make a transfer to another wallet\n4. View all wallets\n5. View all exchange rates\n6. Transaction history\n7. Delete wallets (except EUR)\n8. Exit')

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

    if option == '3':
        print('=' * 46)

        for index, wallet in enumerate(user_wallets):
            print(f'{index + 1}. {wallet}')

        print('=' * 46)
    
        select_first_wallet = input('Select the first wallet (EUR, UAH, etc.): ')
        select_second_wallet = input('Select the second wallet: ')
        amount = input('Enter a amount: ')

        make_a_transfer(select_first_wallet=select_first_wallet, select_second_wallet=select_second_wallet, amount=amount)

    if option == '4':
        print('=' * 46)

        for index, wallet in enumerate(user_wallets):
            print(f'{index + 1}. {wallet}')

        print('=' * 46)

    if option == '5':
        print('=' * 46)

        if len(exchange_rates) == 0:
            print('{:^46}'.format('Empty :)'))
        else:
            for currency, item in exchange_rates.items():
                print(f'{currency}: {item}')

        print('=' * 46)

    if option == '6':
        print('=' * 46)

        for index, transaction in enumerate(transactions):
            print(f'{index + 1}. {transaction}')

        print('=' * 46)

        answer = input('Do you want to create an excel file with transactions? (Yes or No): ')

        if answer.lower() == 'yes':
            sheet = workbook_transaction.active
            sheet.title = 'Transactions'

            for index, transaction in enumerate(transactions):
                sheet[f'A{index + 1}'] = transaction

            workbook_transaction.save("Transactions.xlsx")

            print('The file is saved to the root project folder.')

    if option == '7':
        if len(user_wallets) == 1:
            print('Unable to delete main wallet')
        else:
            answer = input('Are you sure? (Yes or No): ')

            if answer.lower() == 'yes':
                user_wallets.clear()
                exchange_rates.clear()

                create_the_first_wallet(amount=first_amount)

                print(f'Wallets and echange rates have been deleted: {user_wallets}; {exchange_rates}')
                transactions.append(f'Wallets and echange rates have been deleted: {user_wallets}; {exchange_rates}')
    
    if option == '8':
        break