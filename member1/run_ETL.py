import pandas as pd
import os
import sys

# Standardized path initialization
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from config.db_config import get_connection
from member2.init_db import run_schema
from member1.load import load_data
from member1.validate import validate_data
from member1.transform import transform_data
from member1.add_feature import add_features

def run_pipeline(input_file="data/raw/healthcare.csv", skip_schema=False):
    # Step 1: Create tables (only if requested)
    if not skip_schema:
        run_schema()

    # Step 2: Load and Clean
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    df = pd.read_csv(input_file)
    
    # Fast Pre-processing
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    df['Billing Amount'] = df['Billing Amount'].abs()

    # Validation
    validate_data(df)

    # Transform & Features
    df = transform_data(df)
    df = add_features(df)

    # Save and Load
    df.to_csv("data/processed/clean_data.csv", index=False)
    load_data(df)

    print(f"✅ ETL Successful: {input_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="data/raw/healthcare.csv")
    parser.add_argument("--skip-schema", action="store_true")
    args = parser.parse_args()
    
    run_pipeline(args.file, skip_schema=args.skip_schema)
