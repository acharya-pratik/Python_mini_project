def validate_data(df):

    # 🔴 Check missing values
    if df.isnull().sum().sum() > 0:
        raise ValueError("❌ Missing values found!")

    # 🔴 Age must be valid
    if (df['Age'] <= 0).any():
        raise ValueError("❌ Invalid age detected!")

    # 🔴 Billing must be positive
    if (df['Billing Amount'] < 0).any():
        raise ValueError("❌ Negative billing found!")

    # 🔴 Dates logic
    if (df['Discharge Date'] < df['Date of Admission']).any():
        raise ValueError("❌ Invalid dates (discharge before admission)!")

    print("✅ Data validation passed")
    return True
