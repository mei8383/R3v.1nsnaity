import os
import requests
from datetime import datetime
from dotenv import load_dotenv
#from dotreplit import load_dotreplit
# Load environment variables from .env file
load_dotenv()
#load_dotreplit()
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
