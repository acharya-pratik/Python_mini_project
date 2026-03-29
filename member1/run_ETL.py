import pandas as pd
from member2.init_db import run_schema
from member1.load import load_data
from member1.validate import validate_data
from member1.transform import transform_data
from member1.add_feature import add_features

def run_pipeline():

    # Step 1: Create tables
    run_schema()

    # Step 2: Load raw data
    df = pd.read_csv("data/raw/healthcare.csv")

    # Step 3: Convert dates BEFORE validation
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])

    # Fix negative billing amounts
    df['Billing Amount'] = df['Billing Amount'].abs()

    # Step 4: Validate
    validate_data(df)

    # Step 5: Transform
    df = transform_data(df)

    # Step 6: Feature Engineering
    df = add_features(df)

    # Step 7: Save clean data
    df.to_csv("data/processed/clean_data.csv", index=False)

    # Step 8: Load into DB
    load_data(df)

    print("🚀 ETL Pipeline Completed Successfully!")

if __name__ == "__main__":
    run_pipeline()
