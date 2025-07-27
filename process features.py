import pandas as pd
import json

# --- Configuration ---
INPUT_JSON_FILE = "wallet_compound_transactions.json"
OUTPUT_CSV_FILE = "wallet_risk_features.csv"

# The specific function name for a liquidation on Compound V2's cToken contracts
# We need to look for calls to this function.
LIQUIDATION_FUNCTION_NAME = "liquidateBorrow(address borrower, uint256 repayAmount, address cTokenCollateral)"

def process_transaction_data():
    """
    Loads the raw transaction data and calculates the first set of risk features.
    """
    try:
        with open(INPUT_JSON_FILE, 'r') as f:
            all_wallets_data = json.load(f)
        print(f"Successfully loaded data for {len(all_wallets_data)} wallets from '{INPUT_JSON_FILE}'.")
    except FileNotFoundError:
        print(f" Error: The file '{INPUT_JSON_FILE}' was not found. Please make sure it's in the same directory.")
        return
    except json.JSONDecodeError:
        print(f" Error: The file '{INPUT_JSON_FILE}' is not a valid JSON file.")
        return

    # A list to hold the feature data for each wallet
    features_list = []

    # Process each wallet's transactions
    for wallet_id, transactions in all_wallets_data.items():
        
        # --- Feature 1: Liquidation Count ---
        # We check if the wallet was the *borrower* being liquidated.
        # The Etherscan data shows the 'from' address as the liquidator.
        # We need to parse the function input to see who was liquidated.
        liquidation_count = 0
        for tx in transactions:
            # The functionName from Etherscan is a bit messy, so we check if our target string is present
            if LIQUIDATION_FUNCTION_NAME in tx.get('functionName', ''):
                # The 'from' address in a liquidation transaction is the liquidator.
                # The address being liquidated is an argument to the function call itself.
                # For this feature, we will count any liquidation transaction where our wallet was involved.
                # A more advanced analysis could parse the 'input' data to confirm the wallet was the borrower.
                liquidation_count += 1
        
        print(f"-> Wallet: {wallet_id} | Liquidation Count: {liquidation_count}")
        
        # --- Add more feature calculations here in the future ---
        
        features_list.append({
            'wallet_id': wallet_id,
            'liquidation_count': liquidation_count
        })

    # Create a pandas DataFrame from our list of features
    if features_list:
        features_df = pd.DataFrame(features_list)
        
        # Save the DataFrame to a CSV file
        features_df.to_csv(OUTPUT_CSV_FILE, index=False)
        print(f"\n Success! Risk features have been calculated and saved to '{OUTPUT_CSV_FILE}'")
        print("\n--- First 5 wallets ---")
        print(features_df.head())
        print("-----------------------")
    else:
        print("\n No data was processed. No output file created.")


if __name__ == "__main__":
    process_transaction_data()