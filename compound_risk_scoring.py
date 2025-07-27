import pandas as pd
import requests
import time

# === CONFIGURATION ===
COVALENT_API_KEY = "cqt_rQjXmVmJTxxTcc9bVKCm7xJc3Qwt"  # <-- Replace this with your actual API key
CHAIN_ID = 1  # Ethereum mainnet
BASE_URL = "https://api.covalenthq.com/v1"

# === LOAD WALLETS ===
wdf = pd.read_csv("Wallet_id_Sheet1.csv")
wallets = wdf['wallet_id'].str.lower().tolist()

# === DATA STORAGE ===
results = []

def get_compound_transactions(wallet):
    url = f"{BASE_URL}/{CHAIN_ID}/address/{wallet}/transactions_v2/"
    params = {
        "key": COVALENT_API_KEY,
        "page-size": 1000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", {}).get("items", [])
    else:
        print(f"Error fetching data for {wallet}: {response.status_code}")
        return []

def extract_features(wallet, txs):
    # Simple feature extraction based on Compound tx patterns
    borrow = repay = supply = withdraw = 0
    tokens_used = set()

    for tx in txs:
        log_events = tx.get("log_events", [])
        for log in log_events:
            decoded = log.get("decoded")
            if not decoded:
                continue  # skip if decoding is not available

            desc = decoded.get("name", "")
            params = decoded.get("params") or []
            for p in params:
                if p['name'] == 'amount':
                    try:
                        amt = float(p['value']) / 1e18
                    except:
                        amt = 0
                    if desc == 'Borrow':
                        borrow += amt
                    elif desc == 'RepayBorrow':
                        repay += amt
                    elif desc == 'Mint':  # supply
                        supply += amt
                    elif desc == 'Redeem':  # withdraw
                        withdraw += amt

            if "token_0" in log:
                tokens_used.add(log["token_0"])  # rough count

    total = borrow + repay + supply + withdraw
    repayment_ratio = repay / borrow if borrow > 0 else 1
    borrow_supply_ratio = borrow / supply if supply > 0 else 1

    return {
        "wallet": wallet,
        "borrow": borrow,
        "repay": repay,
        "supply": supply,
        "withdraw": withdraw,
        "repayment_ratio": repayment_ratio,
        "borrow_to_supply_ratio": borrow_supply_ratio,
        "unique_tokens_used": len(tokens_used),
        "total_activity": total
    }

# === PROCESS ALL WALLETS ===
for i, wallet in enumerate(wallets):
    print(f"[{i+1}/{len(wallets)}] Processing: {wallet}")
    txs = get_compound_transactions(wallet)
    features = extract_features(wallet, txs)
    results.append(features)
    time.sleep(1)  # Avoid rate limits

# === SCORE CALCULATION ===
df = pd.DataFrame(results)

# Normalize features
df["repayment_ratio"] = df["repayment_ratio"].clip(0, 1)
df["borrow_to_supply_ratio"] = df["borrow_to_supply_ratio"].clip(0, 1)
if df["unique_tokens_used"].max() > 0:
    df["normalized_tokens"] = df["unique_tokens_used"] / df["unique_tokens_used"].max()
else:
    df["normalized_tokens"] = 0

df["normalized_activity"] = df["total_activity"] / df["total_activity"].max()

# Final score

df["risk_score"] = 1000 * (
    0.3 * df["repayment_ratio"].fillna(1) +
    0.2 * (1 - df["borrow_to_supply_ratio"].fillna(1)) +
    0.3 * df["normalized_activity"].fillna(0) +
    0.2 * df["normalized_tokens"].fillna(0)
)


# Save results
df.to_csv("wallet_risk_scores.csv", index=False)
print(" Risk scores saved to wallet_risk_scores.csv")
