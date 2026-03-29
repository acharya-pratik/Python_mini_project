import pandas as pd

def clean_text(df):
    cols = [
        'Name', 'Gender', 'Blood Type', 'Medical Condition',
        'Doctor', 'Hospital', 'Insurance Provider',
        'Medication', 'Test Results', 'Admission Type'
    ]

    for col in cols:
        df[col] = df[col].astype(str).str.strip().str.title()

    return df


def transform_data(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean text
    df = clean_text(df)

    # Convert types
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])

    df['Billing Amount'] = df['Billing Amount'].astype(float)
    df['Age'] = df['Age'].astype(int)

    return df
