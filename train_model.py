import os
import pandas as pd
from src.data_generator import generate_ecommerce_data
from src.ml_engine import train_and_evaluate_models

def main():
    print("====================================================")
    print("🚀 STEP 1: LOADING BENGALURU CUSTOMER SESSIONS DATA")
    print("====================================================")
    if not os.path.exists("data/customer_sessions.csv"):
        generate_ecommerce_data(num_records=25000)

    sessions_df = pd.read_csv("data/customer_sessions.csv")
    print(f"Loaded {len(sessions_df):,} customer sessions.\n")

    print("====================================================")
    print("🌲 STEP 2: TRAINING RANDOM FOREST (100 TREES)")
    print("====================================================")
    rf_model, metrics_df, importance_df, cm = train_and_evaluate_models(sessions_df, save_model=True)
    print("✅ Model trained and saved to: models/random_forest_bundle.pkl\n")

    print("====================================================")
    print("📊 STEP 3: MODEL BENCHMARK COMPARISON (20% TEST SET)")
    print("====================================================")
    print(metrics_df.to_string(index=False))
    print("\n")

    print("====================================================")
    print("🔍 STEP 4: EXPLAINABLE AI — FEATURE IMPORTANCE")
    print("====================================================")
    for _, row in importance_df.iterrows():
        print(f"  • {row['Feature']:<20}: {row['Importance']*100:.2f}%")

if __name__ == "__main__":
    main()