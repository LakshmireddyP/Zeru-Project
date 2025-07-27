import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# --- Configuration ---
INPUT_CSV_FILE = "wallet_risk_features_final.csv"
OUTPUT_CSV_FILE = "wallet_risk_scores.csv"

# Define the features and their corresponding weights
# The weights should sum to 1.0
FEATURE_WEIGHTS = {
    'health_factor_usd': 0.50,
    'liquidation_count': 0.30,
    'account_age_days': 0.10,
    'transaction_count': 0.10 
}

# Define which features are "higher value is better"
# For these, a higher original value should result in a lower risk score.
HIGHER_IS_BETTER = ['health_factor_usd', 'account_age_days']


def calculate_risk_scores():
    """
    Loads the final feature set, normalizes them, and calculates a weighted risk score.
    """
    try:
        df = pd.read_csv(INPUT_CSV_FILE)
        print(f" Successfully loaded features for {len(df)} wallets from '{INPUT_CSV_FILE}'.")
    except FileNotFoundError:
        print(f" Error: The file '{INPUT_CSV_FILE}' was not found. Please run the previous script to generate it.")
        return
        
    # Handle potential missing values, e.g., if a health factor call failed
    df.fillna(0, inplace=True)

    # --- Step 1: Normalize Features ---
    scaler = MinMaxScaler()
    normalized_df = pd.DataFrame(scaler.fit_transform(df[FEATURE_WEIGHTS.keys()]), 
                                 columns=FEATURE_WEIGHTS.keys())
    
    print("\n Normalizing features...")
    # Invert the scores for features where a higher value is better
    for feature in HIGHER_IS_BETTER:
        normalized_df[feature] = 1 - normalized_df[feature]
        print(f"   - Inverted '{feature}' score (so high value = high risk).")

    # --- Step 2: Apply Weights and Calculate Score ---
    print("\n Applying weights and calculating final scores...")
    df['risk_score'] = 0
    for feature, weight in FEATURE_WEIGHTS.items():
        df['risk_score'] += normalized_df[feature] * weight
        
    # --- Step 3: Scale to 0-1000 ---
    # The risk_score is currently between 0 and 1. We scale it to 0-1000.
    df['score'] = (df['risk_score'] * 1000).astype(int)
    
    # --- Step 4: Final Output ---
    final_output_df = df[['wallet_id', 'score']]
    
    # Sort by score, highest risk first
    final_output_df = final_output_df.sort_values(by='score', ascending=False)
    
    # Save the final scores to a new CSV file
    final_output_df.to_csv(OUTPUT_CSV_FILE, index=False)
    
    print(f"\n Success! Final risk scores calculated and saved to '{OUTPUT_CSV_FILE}'.")
    print("\n--- Top 5 Highest-Risk Wallets ---")
    print(final_output_df.head())
    print("------------------------------------")
    print("\n--- Top 5 Lowest-Risk Wallets ---")
    print(final_output_df.tail())
    print("-----------------------------------")


if __name__ == "__main__":
    calculate_risk_scores()