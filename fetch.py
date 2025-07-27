import pandas as pd
import requests
import json
import time

# --- Configuration ---
# 1. PASTE YOUR ETHERSCAN API KEY HERE
API_KEY = "8D9YARP3UXXWNHXPKAA9JSTQZWAZ69VFEU"

# 2. Etherscan API Endpoint
API_ENDPOINT = "https://api.etherscan.io/api"

# 3. Compound V2 Contract Addresses (Key contracts for filtering)
# We are interested in transactions that interact with these addresses.
COMPOUND_CONTRACTS = {
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b".lower(),  # Comptroller
    "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5".lower(),  # cETH
    "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643".lower(),  # cDAI
    "0x39aa39c021dfbae8fac545936693ac917d5e7563".lower(),  # cUSDC
    "0x158079ee67fce2f58472a96584a73c7ab9ac95c1".lower(),  # cREP
    "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9".lower(),  # cBAT
    "0xc11b1268c1a384e55c48c2391d8d480264a3a7f4".lower(),  # cZRX
    "0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407".lower(),  # cSAI
    "0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e".lower(),  # cBAT (old)
}

INPUT_CSV_FILE = "Wallet id - Sheet1.csv"
OUTPUT_JSON_FILE = "wallet_compound_transactions.json"

def fetch_wallet_transactions(wallet_id):
    """Fetches all transactions for a single wallet from Etherscan."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_id,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": API_KEY
    }
    try:
        response = requests.get(API_ENDPOINT, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1':
                return data['result']
            else:
                # This could be a rate limit or "No transactions found"
                print(f" -> Etherscan API Message for {wallet_id}: {data['message']}")
                return []
        else:
            print(f" -> HTTP Error for {wallet_id}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f" -> Network error for {wallet_id}: {e}")
        return None

def main():
    """Main function to read IDs, fetch data, filter, and save."""
    if API_KEY == "YOUR_ETHERSCAN_API_KEY" or not API_KEY:
        print("🚨 Error: Please paste your Etherscan API key into the script.")
        return

    try:
        wallets_df = pd.read_csv(INPUT_CSV_FILE)
        wallet_ids = wallets_df['wallet_id'].tolist()
        print(f"Found {len(wallet_ids)} wallet IDs to process.")
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_CSV_FILE}' was not found.")
        return
    except KeyError:
        print(f"Error: CSV file must have a column named 'wallet_id'.")
        return

    all_compound_txs = {}
    total_processed = 0

    for wallet_id in wallet_ids:
        print(f"Processing {wallet_id}...")
        transactions = fetch_wallet_transactions(wallet_id)
        total_processed += 1
        
        if transactions is not None:
            # Filter the transactions to find Compound V2 interactions
            compound_txs = [
                tx for tx in transactions 
                if tx.get('to', '').lower() in COMPOUND_CONTRACTS
            ]
            
            if compound_txs:
                print(f" ->  Found {len(compound_txs)} Compound V2 transaction(s) for {wallet_id}")
                all_compound_txs[wallet_id] = compound_txs
            else:
                print(f" ->  No Compound V2 transactions found for {wallet_id}")

        # Etherscan has a rate limit (5 calls/sec for free tier), so we pause
        time.sleep(0.25)

    if all_compound_txs:
        with open(OUTPUT_JSON_FILE, 'w') as f:
            json.dump(all_compound_txs, f, indent=4)
        print(f"\n Success! All Compound V2 transaction data has been saved to '{OUTPUT_JSON_FILE}'")
    else:
        print(f"\n No wallets with Compound V2 transaction history were found. No file was created.")

    print(f"\n--- Summary ---")
    print(f"Total wallets processed: {total_processed}")
    print(f"Wallets with Compound V2 data: {len(all_compound_txs)}")
    print("---------------")

if __name__ == "__main__":
    main()