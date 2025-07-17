import pandas as pd

def assign_credit_score(row):
    score = 300

    score += min(row["total_deposit_usd"] / 100, 200)
    score += min(row["total_repay_usd"] / 100, 200)
    score += min(row["tx_per_day"] * 10, 100)
    
    score += (1 - min(row["redeem_ratio"], 1.0)) * 100
    score += (1 - min(row["repay_ratio"], 1.0)) * 100

    score -= row["num_liquidations"] * 50

    return max(0, min(1000, score))  # Clamp between 0 and 1000

def add_credit_scores(input_csv="wallet_features.csv", output_csv="wallet_features.csv"):
    df = pd.read_csv(input_csv)
    df["credit_score"] = df.apply(assign_credit_score, axis=1)
    df.to_csv(output_csv, index=False)
    print(f"✅ Added credit_score column and saved to {output_csv}")

if __name__ == "__main__":
    add_credit_scores()
