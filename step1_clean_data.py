import json
import pandas as pd
from datetime import datetime

def load_and_clean(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    records = []
    for entry in data:
        try:
            wallet = entry["userWallet"]
            ts = entry["timestamp"]
            action = entry["action"].lower()
            amt = float(entry["actionData"]["amount"])
            price = float(entry["actionData"]["assetPriceUSD"])
            usd_value = amt * price
            records.append({
                "wallet_address": wallet,
                "timestamp": datetime.utcfromtimestamp(ts),
                "action": action,
                "usd_value": usd_value
            })
        except (KeyError, ValueError, TypeError):
            continue  # Skip invalid records

    df = pd.DataFrame(records)
    return df

# Example usage:
if __name__ == "__main__":
    path_to_json = "user-wallet-transactions.json"
    df = load_and_clean(path_to_json)
    print(df.head())
    df.to_csv("cleaned_transactions.csv", index=False)
    print("✅ Cleaned data saved to cleaned_transactions.csv")
