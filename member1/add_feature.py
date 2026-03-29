import pandas as pd

def add_features(df):

    # Hospital Stay Days
    df['Hospital_Stay_Days'] = (
        df['Discharge Date'] - df['Date of Admission']
    ).dt.days

    # Age Group
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0, 18, 40, 60, 120],
        labels=['Child', 'Adult', 'Middle_Age', 'Senior']
    )

    # Billing Category
    df['Billing_Category'] = pd.cut(
        df['Billing Amount'],
        bins=[0, 15000, 30000, 100000],
        labels=['Low', 'Medium', 'High']
    )

    # Long Stay Flag
    df['Long_Stay'] = df['Hospital_Stay_Days'].apply(
        lambda x: 1 if x > 7 else 0
    )

    return df
