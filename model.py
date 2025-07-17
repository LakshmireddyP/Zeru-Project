import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

FEATURES = [
    "total_tx", "duration_days", "tx_per_day",
    "total_deposit_usd", "total_borrow_usd",
    "total_repay_usd", "total_redeem_usd",
    "repay_ratio", "redeem_ratio", "num_liquidations"
]

def train_credit_model(csv_path="wallet_features.csv", output_model="credit_model.pkl"):
    df = pd.read_csv(csv_path)
    if "credit_score" not in df.columns:
        raise ValueError("Missing 'credit_score' column. Run step3_score_wallets.py first.")

    X = df[FEATURES]
    y = df["credit_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, preds):.2f}")
    print(f"R² Score: {r2_score(y_test, preds):.3f}")

    # Save model
    joblib.dump(model, output_model)
    print(f"✅ Model saved to {output_model}")

if __name__ == "__main__":
    train_credit_model()
