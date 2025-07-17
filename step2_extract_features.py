import pandas as pd

def extract_wallet_features(df):
    df = df.sort_values(by=["wallet_address", "timestamp"])

    feature_list = []

    for wallet, group in df.groupby("wallet_address"):
        timestamps = group["timestamp"]
        actions = group["action"]
        usd_values = group["usd_value"]

        total_tx = len(group)
        duration_days = (timestamps.max() - timestamps.min()).days + 1
        tx_per_day = total_tx / duration_days if duration_days > 0 else total_tx

        total_deposit = group[group["action"] == "deposit"]["usd_value"].sum()
        total_borrow = group[group["action"] == "borrow"]["usd_value"].sum()
        total_repay = group[group["action"] == "repay"]["usd_value"].sum()
        total_redeem = group[group["action"] == "redeemunderlying"]["usd_value"].sum()
        num_liquidations = len(group[group["action"] == "liquidationcall"])
        # Count-based features
        num_deposits = group[group['action'] == 'deposit'].groupby('wallet_address').size().rename('num_deposits')
        num_borrows = group[group['action'] == 'borrow'].groupby('wallet_address').size().rename('num_borrows')
        num_repays = group[group['action'] == 'repay'].groupby('wallet_address').size().rename('num_repays')
        num_redeems = group[group['action'] == 'redeemunderlying'].groupby('wallet_address').size().rename('num_redeems')
        # Count number of unique days each wallet is active
        group['date'] = pd.to_datetime(df['timestamp'], unit='s')
        active_days = group.groupby('wallet_address')['date'].nunique().rename('active_days')



        repay_ratio = min(1.0, total_repay / total_borrow) if total_borrow > 0 else 1.0
        redeem_ratio = min(1.0, total_redeem / total_deposit) if total_deposit > 0 else 1.0

        feature_list.append({
            "wallet_address": wallet,
            "total_tx": total_tx,
            "duration_days": duration_days,
            "tx_per_day": tx_per_day,
            "total_deposit_usd": total_deposit,
            "total_borrow_usd": total_borrow,
            "total_repay_usd": total_repay,
            "total_redeem_usd": total_redeem,
            "repay_ratio": repay_ratio,
            "redeem_ratio": redeem_ratio,
            "num_liquidations": num_liquidations,
            "num_deposits":num_deposits,
            "num_borrows":num_borrows,
            "num_repays":num_repays,
            "num_redeems":num_redeems,
            "active_days":active_days

        })

    return pd.DataFrame(feature_list)

# Example usage
if __name__ == "__main__":
    df = pd.read_csv("cleaned_transactions.csv", parse_dates=["timestamp"])
    feature_df = extract_wallet_features(df)
    print(feature_df.head())
    feature_df.to_csv("wallet_features.csv", index=False)
    print("✅ Wallet features saved to wallet_features.csv")
