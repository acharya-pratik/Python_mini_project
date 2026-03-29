import pandas as pd

def clean_text(df):
    cols = [
        'Name', 'Gender', 'Blood Type', 'Medical Condition',
        'Doctor', 'Hospital', 'Insurance Provider',
        'Medication', 'Test Results', 'Admission Type'
    ]

    for col in cols:
        if col in df.columns:
            df.loc[:, col] = df[col].astype(str).str.strip().str.title()

    return df


def transform_data(df):
    # Ensure we work on a copy to avoid SettingWithCopyWarning
    df = df.copy()

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean text
    df = clean_text(df)

    # Convert types
    df.loc[:, 'Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df.loc[:, 'Discharge Date'] = pd.to_datetime(df['Discharge Date'])

    df.loc[:, 'Billing Amount'] = df['Billing Amount'].astype(float)
    df.loc[:, 'Age'] = df['Age'].astype(int)

    return df
