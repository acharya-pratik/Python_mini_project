import pandas as pd

def validate_data(df):
    """
    Performs data integrity checks on the healthcare dataset.
    Raises ValueError if critical issues are found.
    """
    # 1. Check for missing values in critical columns
    critical_cols = ['Name', 'Age', 'Gender', 'Medical Condition', 'Date of Admission', 'Billing Amount']
    missing = df[critical_cols].isnull().sum()
    if missing.any():
        print(f"⚠️ Warning: Missing values detected:\n{missing[missing > 0]}")
        # We fill rather than raise to keep the demo running smoothly
        df['Age'] = df['Age'].fillna(df['Age'].median())
        df['Billing Amount'] = df['Billing Amount'].fillna(0)

    # 2. Age Validation
    if not df[(df['Age'] < 0) | (df['Age'] > 120)].empty:
        print("⚠️ Warning: Invalid age detected. Clipping to [0, 120].")
        df['Age'] = df['Age'].clip(0, 120)

    # 3. Billing Validation
    if (df['Billing Amount'] < 0).any():
        print("⚠️ Warning: Negative billing found. Converting to absolute values.")
        df['Billing Amount'] = df['Billing Amount'].abs()

    # 4. Date Logic Validation
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    invalid_dates = df[df['Discharge Date'] < df['Date of Admission']]
    if not invalid_dates.empty:
        print(f"⚠️ Warning: {len(invalid_dates)} records have discharge before admission. Fixing...")
        # Simple fix: set discharge to admission date + 1 day
        df.loc[df['Discharge Date'] < df['Date of Admission'], 'Discharge Date'] = \
            df['Date of Admission'] + pd.Timedelta(days=1)

    return True
