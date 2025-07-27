import pandas as pd
import json
from datetime import datetime

# --- Configuration ---
INPUT_JSON_FILE = "wallet_compound_transactions.json"
OUTPUT_CSV_FILE = "wallet_risk_features.csv" # We will overwrite the previous file with the new features

def process_and_enhance_features():
    """
    Loads transaction data and calculates transaction count and account age.
    """
    try:
        with open(INPUT_JSON_FILE, 'r') as f:
            all_wallets_data = json.load(f)
        print(f" Successfully loaded data for {len(all_wallets_data)} wallets.")
    except FileNotFoundError:
        print(f" Error: The file '{INPUT_JSON_FILE}' was not found.")
        return

    features_list = []

    # Process each wallet's transactions
    for wallet_id, transactions in all_wallets_data.items():
        
        # --- Feature 2: Transaction Count ---
        transaction_count = len(transactions)

        # --- Feature 3: Account Age in Days ---
        if transaction_count > 0:
            # Timestamps are in UNIX format, so we convert them to numbers
            timestamps = [int(tx['timeStamp']) for tx in transactions]
            first_tx_timestamp = min(timestamps)
            # Get the current time to calculate age
            current_timestamp = int(datetime.now().timestamp())
            # Calculate the difference in seconds and convert to days
            account_age_days = (current_timestamp - first_tx_timestamp) / (60 * 60 * 24)
        else:
            account_age_days = 0

        print(f"-> Wallet: {wallet_id} | Transactions: {transaction_count} | Age (Days): {account_age_days:.0f}")

        features_list.append({
            'wallet_id': wallet_id,
            'transaction_count': transaction_count,
            'account_age_days': int(account_age_days)
            # We'll add liquidation_count back in the next step
        })

    # Create a new DataFrame with our new features
    if features_list:
        new_features_df = pd.DataFrame(features_list)
        
        # --- Merge with Existing Features ---
        try:
            # Load the original features file that has the liquidation_count
            existing_features_df = pd.read_csv(OUTPUT_CSV_FILE)
            
            # Merge the new features with the existing ones based on wallet_id
            final_df = pd.merge(existing_features_df, new_features_df, on='wallet_id')
            
            # Reorder columns for clarity
            final_df = final_df[['wallet_id', 'liquidation_count', 'transaction_count', 'account_age_days']]

            # Save the final combined DataFrame
            final_df.to_csv(OUTPUT_CSV_FILE, index=False)
            
            print(f"\n Success! New features calculated and merged into '{OUTPUT_CSV_FILE}'")
            print("\n--- First 5 wallets (Updated) ---")
            print(final_df.head())
            print("---------------------------------")
            
        except FileNotFoundError:
            print(f" Error: The original '{OUTPUT_CSV_FILE}' was not found. Please run the previous script first.")
            return

    else:
        print("\n No data was processed.")

if __name__ == "__main__":
    process_and_enhance_features()