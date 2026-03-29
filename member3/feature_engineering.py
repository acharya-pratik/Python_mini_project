import pandas as pd
from sklearn.preprocessing import LabelEncoder

def prepare_features(df, task="high_billing"):
    """
    Prepares features for ML models.
    Handles categorical encoding and feature creation.
    """
    df = df.copy()

    # --- Feature Engineering ---
    if 'Date of Admission' in df.columns and 'Discharge Date' in df.columns:
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
        df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
        df['Hospital_Stay_Days'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
        df['Long_Stay'] = df['Hospital_Stay_Days'].apply(lambda x: 1 if x > 7 else 0)

    # --- Encode Categorical Variables ---
    if 'Gender' in df.columns:
        gender_map = {'Male': 0, 'Female': 1, 'Other': -1}
        df['Gender_Encoded'] = df['Gender'].map(gender_map).fillna(-2)
    else:
        df['Gender_Encoded'] = -1

    if 'Blood Type' in df.columns:
        blood_map = {'A+':1,'A-':2,'B+':3,'B-':4,'AB+':5,'AB-':6,'O+':7,'O-':8}
        df['Blood_Type_Encoded'] = df['Blood Type'].map(blood_map).fillna(0)
    else:
        df['Blood_Type_Encoded'] = 0

    if 'Admission Type' in df.columns:
        admission_map = {'Elective':0,'Urgent':1,'Emergency':2}
        df['Admission_Type_Encoded'] = df['Admission Type'].map(admission_map).fillna(-1)
    else:
        df['Admission_Type_Encoded'] = -1

    if 'Medical Condition' in df.columns:
        condition_map = {'Cancer':0, 'Obesity':1, 'Diabetes':2, 'Asthma':3, 'Hypertension':4, 'Arthritis':5}
        df['Condition_Encoded'] = df['Medical Condition'].map(condition_map).fillna(-1)
    else:
        df['Condition_Encoded'] = -1

    # --- Define Features ---
    features = [
        'Age', 'Gender_Encoded', 'Blood_Type_Encoded', 
        'Condition_Encoded', 'Admission_Type_Encoded'
    ]
    
    # Filter DataFrame to only include required features
    X = df.reindex(columns=features, fill_value=0)

    # --- Define Targets ---
    y = None
    if task == "high_billing":
        if 'Billing Amount' in df.columns:
            threshold = 30000 
            df['High_Billing'] = df['Billing Amount'].apply(lambda x: 1 if x > threshold else 0)
            y = df['High_Billing']
        else:
            y = pd.Series([0] * len(df))
            
    elif task == "length_of_stay":
        if 'Hospital_Stay_Days' in df.columns:
            y = df['Hospital_Stay_Days']
        else:
            y = pd.Series([0] * len(df))
    
    if y is None:
        raise ValueError(f"Target variable 'y' could not be determined for task: {task}")

    return X, y
