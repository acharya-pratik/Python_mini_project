import pandas as pd
import numpy as np

def add_features(df):
    """
    Optimized feature engineering using vectorized pandas/numpy operations.
    Adds hospital stay duration, age groups, and billing categories.
    """
    # 1. Hospital Stay Days (Vectorized subtraction)
    df['Hospital_Stay_Days'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
    # Set minimum stay to 0 to avoid negative values
    df['Hospital_Stay_Days'] = df['Hospital_Stay_Days'].clip(0)

    # 2. Age Group (Optimized with pd.cut)
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0, 18, 40, 60, 120],
        labels=['Child', 'Adult', 'Middle_Age', 'Senior']
    )

    # 3. Billing Category (Optimized with pd.cut)
    df['Billing_Category'] = pd.cut(
        df['Billing Amount'],
        bins=[-np.inf, 15000, 30000, np.inf],
        labels=['Low', 'Medium', 'High']
    )

    # 4. Long Stay Flag (Optimized with vectorized comparison)
    df['Long_Stay'] = (df['Hospital_Stay_Days'] > 7).astype(int)

    return df
