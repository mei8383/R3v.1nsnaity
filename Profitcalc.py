import requests
from datetime import datetime

# Replace these with your actual API keys
HELIUS_API_KEY = '2a0818be-6981-48c5-b228-048294a1134a'
BIRDEYE_API_KEY = 'abfa609c4d9542129fbe5c77c4c35e4a'

# Helius API endpoint to get wallet transactions
HELIUS_API_URL = 'https://api.helius.xyz/v1/transactions'

# Birdeye API endpoint to get token price
BIRDEYE_API_URL = 'https://api.birdeye.so/v1/price'

# Function to get wallet transactions from Helius
def get_wallet_transactions(wallet_address):
    url = f'{HELIUS_API_URL}/{wallet_address}'
    headers = {'Authorization': f'Bearer {HELIUS_API_KEY}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Error fetching Helius transactions: {response.status_code}")
        return []

# Function to get token price from Birdeye
def get_token_price(token_symbol, timestamp):
    # Convert timestamp to the format Birdeye expects
    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').timestamp()
    
    params = {
        'symbol': token_symbol,
        'timestamp': int(timestamp),
        'apiKey': BIRDEYE_API_KEY
    }
    
    response = requests.get(BIRDEYE_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'price' in data:
            return float(data['price'])
        else:
            print(f"No price data for {token_symbol} at {timestamp}")
            return None
    else:
        print(f"Error fetching Birdeye price data: {response.status_code}")
        return None

# Function to calculate profitability based on transactions
def calculate_profit_from_transactions(wallet_address):
    transactions = get_wallet_transactions(wallet_address)
    total_profit = 0
    total_spent = 0

    for tx in transactions:
        token_symbol = tx['tokenSymbol']  # The token symbol (e.g., 'SOL', 'USDC')
        direction = tx['direction']  # 'in' for buy, 'out' for sell
        amount = float(tx['amount'])  # Amount of tokens involved
        timestamp = tx['timestamp']  # Transaction timestamp

        # Get the token price from Birdeye at the time of transaction
        token_price = get_token_price(token_symbol, timestamp)
        
        if token_price is None:
            continue  # If the price isn't available, skip this transaction

        transaction_value = amount * token_price  # Value of the transaction at the time
        
        # If it's a buy (token comes into the wallet)
        if direction == 'in':
            total_spent += transaction_value  # Add to total spent
        # If it's a sell (token goes out of the wallet)
        elif direction == 'out':
            total_profit += transaction_value  # Add to total profit

    # Calculate net profit
    net_profit = total_profit - total_spent
    return net_profit

# Example usage
if __name__ == "__main__":
    wallet_address = "your_wallet_address_here"  # Replace with the actual wallet address
    profit = calculate_profit_from_transactions(wallet_address)
    print(f"Net Profit: {profit}")
