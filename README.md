# DeFi Wallet Credit Scoring System

This project implements a machine learning-based credit scoring system for wallets, assigning a **score from 0 to 1000** based solely on historical DeFi transaction behavior.

---

## 🔍 Overview

Each wallet is scored based on activity patterns like deposits, borrows, repayments, and redemptions. Higher scores reflect responsible and stable behavior. Lower scores indicate bot-like, high-risk, or exploitative behavior.

The scoring system is trained on real wallet feature data and can process raw transaction history JSON in a single step.

---

## 📊 Features Used

We engineered the following features per wallet from DeFi transaction data:

| Feature               | Description |
|-----------------------|-------------|
| `total_tx`            | Total number of transactions |
| `duration_days`       | Time span between first and last transaction |
| `tx_per_day`          | Normalized transaction frequency |
| `total_deposit_usd`   | Total deposits in USD |
| `total_borrow_usd`    | Total borrowed in USD |
| `total_repay_usd`     | Total repayments in USD |
| `total_redeem_usd`    | Total redemptions in USD |
| `repay_ratio`         | Repayments divided by borrows |
| `redeem_ratio`        | Redemptions divided by deposits |
| `num_liquidations`    | Number of liquidation events (penalty) |
| `num_deposits`        | Count of deposit transactions |
| `num_borrows`         | Count of borrow transactions |
| `num_repays`          | Count of repay transactions |
| `num_redeems`         | Count of redeem transactions |
| `active_days`         | Days wallet was active |

These features aim to capture:
- **Reliability** (repay_ratio, redeem_ratio)
- **Activity consistency** (tx_per_day, active_days)
- **Risk exposure** (num_liquidations)
- **Usage variety** (engagement in multiple DeFi activities)

---

## 🧠 Model

A **RandomForestRegressor** was trained using `sklearn` to predict a credit score in the range **0–1000**. The model is saved as `credit_model.pkl`.

### Evaluation Metrics:
- **Mean Absolute Error (MAE)**: 2.49 ~low error on test set
- **R² Score**: 0.994  Strong predictive performance (check output during training)

---

## 🚀 Usage

### Step 1: Train the model (once)
```bash
python model.py  # trains on wallet_features.csv
