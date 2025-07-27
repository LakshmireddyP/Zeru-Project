import pandas as pd
from web3 import Web3

# --- Configuration ---
# 1. PASTE YOUR ALCHEMY HTTPS URL HERE
ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/WSgAmAa3YtZKv8Ni2RFAh"

# 2. Compound V2 Comptroller Contract Address
COMPTROLLER_ADDRESS = "0x3d9819210A31B4961B30EF54bE2AEd79B9c9Cd3B"

# 3. We only need the ABI for the one function we're calling: getAccountLiquidity
COMPTROLLER_ABI = """
[
  {
    "constant": true,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getAccountLiquidity",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      },
      {
        "name": "",
        "type": "uint256"
      },
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
"""

# The file with historical features we've already built
INPUT_CSV_FILE = "wallet_risk_features.csv" 
# The final output file with all features
OUTPUT_CSV_FILE = "wallet_risk_features_final.csv" 

def get_live_health_factor():
    """
    Connects to the blockchain and fetches the live health factor for each wallet.
    """
    if "YOUR_ALCHEMY_HTTPS_URL" in ALCHEMY_URL:
        print(" Error: Please paste your Alchemy HTTPS URL into the ALCHEMY_URL variable.")
        return

    # Connect to the Ethereum network
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
    if not w3.is_connected():
        print(" Error: Could not connect to Ethereum network. Check your Alchemy URL.")
        return
    print(" Successfully connected to the Ethereum network via Alchemy.")

    # Create a contract object to interact with
    comptroller_contract = w3.eth.contract(address=Web3.to_checksum_address(COMPTROLLER_ADDRESS), abi=COMPTROLLER_ABI)
    
    # --- Load our existing feature data ---
    try:
        features_df = pd.read_csv(INPUT_CSV_FILE)
        wallet_ids = features_df['wallet_id'].tolist()
    except FileNotFoundError:
        print(f" Error: The file '{INPUT_CSV_FILE}' was not found. Please run the previous feature engineering scripts first.")
        return
    
    health_factors = []

    print("\nFetching live health factors for each wallet...")
    for wallet_id in wallet_ids:
        try:
            # Call the smart contract function which returns: (error, liquidity, shortfall)
            # 'liquidity' is the user's Health Factor in USD (their safety cushion).
            # 'shortfall' is how much they are underwater (if > 0).
            error, liquidity, shortfall = comptroller_contract.functions.getAccountLiquidity(Web3.to_checksum_address(wallet_id)).call()
            
            # Convert from Wei (the base unit of Ether) to a regular number
            liquidity_usd = float(w3.from_wei(liquidity, 'ether'))
            shortfall_usd = float(w3.from_wei(shortfall, 'ether'))

            # We define our health_factor as the liquidity. If there's a shortfall, it's a negative health factor.
            health_factor = liquidity_usd if shortfall_usd == 0 else -shortfall_usd
            
            print(f"-> Wallet: {wallet_id} | Health Factor (USD): {health_factor:,.2f}")
            health_factors.append(health_factor)
            
        except Exception as e:
            print(f" ->  Error fetching data for {wallet_id}: {e}")
            health_factors.append(None)

    # Add the new feature to our DataFrame
    features_df['health_factor_usd'] = health_factors
    
    # Save the final DataFrame
    features_df.to_csv(OUTPUT_CSV_FILE, index=False)
    print(f"\n Success! Live health factors calculated and saved to '{OUTPUT_CSV_FILE}'")
    print("\n--- Final Features (First 5 Wallets) ---")
    print(features_df.head())
    print("------------------------------------------")


if __name__ == "__main__":
    get_live_health_factor()