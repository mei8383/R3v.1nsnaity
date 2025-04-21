import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access API keys securely
HELIUS_API_KEY = os.getenv('HELIUS_API_KEY')
BIRDEYE_API_KEY = os.getenv('BIRDEYE_API_KEY')

# Helius and Birdeye API URLs
HELIUS_API_URL = 'https://api.helius.xyz/v1/transactions'
BIRDEYE_API_URL = 'https://api.birdeye.so/v1/price'

# Function to get wallet transactions from Helius
def get_wallet_transactions(wallet_address):
    url = f'{HELIUS_API_URL}/{wallet_address}'
    headers = {'Authorization': f'Bearer {HELIUS_API_KEY}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Helius transactions: {e}")
        return []

# Function to get token price from Birdeye
def get_token_price(token_symbol, timestamp):
    try:
        # Convert timestamp to the format Birdeye expects
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').timestamp()
        params = {
            'symbol': token_symbol,
            'timestamp': int(timestamp),
            'apiKey': BIRDEYE_API_KEY
        }
        response = requests.get(BIRDEYE_API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        data = response.json()
        return float(data['price']) if 'price' in data else None
    except ValueError as ve:
        print(f"Invalid timestamp format: {ve}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Birdeye price data: {e}")
        return None

# Function to calculate profitability from transactions
def calculate_profit_from_transactions(wallet_address):
    transactions = get_wallet_transactions(wallet_address)
    if not transactions:
        print("No transactions found.")
        return 0

    total_profit = 0
    total_spent = 0

    for tx in transactions:
        try:
            token_symbol = tx['tokenSymbol']
            direction = tx['direction']
            amount = float(tx['amount'])
            timestamp = tx['timestamp']
            token_price = get_token_price(token_symbol, timestamp)

            if token_price is None:
                continue

            transaction_value = amount * token_price
            if direction == 'in':
                total_spent += transaction_value
            elif direction == 'out':
                total_profit += transaction_value
        except KeyError as ke:
            print(f"Transaction data missing key: {ke}")
            continue

    return total_profit - total_spent

# Example usage
if __name__ == "__main__":
    wallet_address = input("your_wallet_address_here") # Replace with your wallet address
    profit = calculate_profit_from_transactions(wallet_address)
    print(f"Net Profit: {profit}")
