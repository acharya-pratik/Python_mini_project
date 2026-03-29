import os
import subprocess
import sys
import pandas as pd
from member4.db import load_data as load_from_db

def run_step(name, command):
    print(f"\n--- Running Step: {name} ---")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Step '{name}' failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"✅ Step '{name}' completed successfully")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="data/raw/healthcare.csv", help="Input file for ETL")
    args = parser.parse_args()
    
    print("🏥 Healthcare Analytics Project Main Runner")

    # Step 1: Run ETL (ensure main data is in DB)
    run_step("ETL Pipeline", f"python3 -m member1.run_ETL --file {args.file}")

    # Step 2: Extract TOTAL data from DB for Training
    print("\n--- 📦 Extracting Total Data from Database for Training ---")
    try:
        df_total = load_from_db()
        df_total.to_csv("data/processed/clean_data.csv", index=False)
        print(f"✅ Extracted {len(df_total)} records for training.")
    except Exception as e:
        print(f"❌ Failed to extract data from DB: {e}")
        sys.exit(1)

    # Step 3: ML Training on the Total Data
    run_step("ML Training - High Billing", "python3 -m member3.train_high_billing")
    run_step("ML Training - Length of Stay", "python3 -m member3.train_length_of_stay")

    # Step 4: Evaluation
    run_step("ML Evaluation", "python3 -m member3.evaluate")

    print("\n🚀 All steps completed successfully!")
    print("\n1. To start the LIVE DEMO: python3 automation_runner.py")
    print("2. To see the DASHBOARD: streamlit run member4/app.py")

if __name__ == "__main__":
    main()
