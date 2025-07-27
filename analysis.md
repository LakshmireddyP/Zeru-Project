# Wallet Credit Score Analysis

This document presents an analysis of credit scores generated for wallets based on their DeFi transaction behavior. The credit scores range from 0 to 1000, where:

- **Higher scores** indicate trustworthy, stable, and responsible wallet behavior.
- **Lower scores** highlight risky, bot-like, or exploitative patterns.

---

##  Score Distribution

The wallets have been categorized into the following score ranges:

- 0–100      -0
- 101–200    -1
- 201–300    -2
- 301–400    -28
- 401–500    -12
- 501–600    -66
- 601–700    -338
- 701–800    -317
- 801–900    -165
- 901–1000   -71

A histogram of the distribution is plotted below:

                            Wallet Score Distribution

101-200 |                                         (0.1%)

201-300 |                                         (0.2%)

301-400 | █▋                                      (2.8%)

401-500 | ▋                                       (1.2%)

501-600 | ████                                    (6.6%)

601-700 | ████████████████████████████████████████  (33.8%)

701-800 | █████████████████████████████████         (31.7%)

801-900 | ████████████████                          (16.5%)

901-1000| ████▍                                   (7.1%)

> _The histogram illustrates the count of wallets falling into each credit score bucket._

---

##  Behavioral Insights by Score Range

###  0–200 (High Risk)

- **Behavior:** These wallets typically show erratic or extremely short-lived activity. Indicators include:
  - Very low total transaction count
  - Abnormally high borrow without corresponding repayment
  - A low redeem/repay ratio
  - Low active days or usage bursts
- **Inference:** Likely bots, exploiters, or throwaway wallets.

---

###  201–500 (Moderate Risk)

- **Behavior:** Inconsistent usage patterns:
  - Few deposits compared to withdrawals
  - Occasional repayments but below average ratios
  - Limited active days and liquidity interactions
- **Inference:** These wallets may belong to occasional users or testing wallets. They show some utility, but reliability is questionable.

---

###  501–800 (Low Risk)

- **Behavior:** These wallets maintain stable and balanced interactions:
  - Reasonable number of transactions
  - Positive repay/redeem ratios
  - Active over multiple days or months
- **Inference:** Possibly real users with fair engagement in DeFi protocols.

---

### 801–1000 (Very Low Risk / Trusted)

- **Behavior:**
  - High and consistent transaction volumes
  - Good repay and redeem behavior
  - Long active durations
  - Low or zero liquidation history
- **Inference:** Strong indication of responsible wallet usage. Could be long-term investors or experienced DeFi users.

---

##  Conclusion

The scoring system provides a clear separation between high-risk and trustworthy wallets based on on-chain behavior patterns. It can be extended with:

- More granular features (e.g., protocol-specific metrics)
- Time series behavior trends
- Integration with risk labels (fraudulent/exploiter tagging)

---

##  Notes

- Source File: `predicted_wallet_scores.csv`
- Score Range: 0 (worst) to 1000 (best)
- Scoring Model: `RandomForestRegressor` trained on transaction-derived features

