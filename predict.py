# predict.py

import pandas as pd
import joblib

def predict_credit_scores():
    # Load features and trained model
    df = pd.read_csv("wallet_features.csv")
    model = joblib.load("credit_model.pkl")

    # Define features used during training
    feature_cols = [
    "total_tx", "duration_days", "tx_per_day",
    "total_deposit_usd", "total_borrow_usd",
    "total_repay_usd", "total_redeem_usd",
    "repay_ratio", "redeem_ratio", "num_liquidations"
]

    # Make predictions
    df['predicted_credit_score'] = model.predict(df[feature_cols])

    # Round and clip scores between 0 and 1000
    df['predicted_credit_score'] = df['predicted_credit_score'].round().clip(0, 1000)

    # Save results
    df[['wallet_address', 'predicted_credit_score']].to_csv("predicted_wallet_scores.csv", index=False)
    print("✅ Predicted scores saved to predicted_wallet_scores.csv")

if __name__ == "__main__":
    predict_credit_scores()
