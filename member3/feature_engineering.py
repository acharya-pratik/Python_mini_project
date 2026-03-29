import pandas as pd
from sklearn.preprocessing import LabelEncoder

def prepare_features(df, task="high_billing"):
    """
    Prepares features for ML models.
    Handles categorical encoding and feature creation.
    """
    df = df.copy()

    # --- Feature Engineering ---
    # Ensure Date columns are datetime objects for stay calculation
    if 'Date of Admission' in df.columns and 'Discharge Date' in df.columns:
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
        df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
        df['Hospital_Stay_Days'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
        df['Long_Stay'] = df['Hospital_Stay_Days'].apply(lambda x: 1 if x > 7 else 0)
    else:
        # Handle cases where dates might be missing for prediction input
        # For prediction, we might need default values or to skip if essential dates are missing
        # For now, assume they exist or will be handled by input form.
        pass

    # --- Encode Categorical Variables ---
    # Gender mapping
    if 'Gender' in df.columns:
        # Map 'Male', 'Female', and 'Other' (or any other value) to numerical representations
        gender_map = {'Male': 0, 'Female': 1, 'Other': -1}
        df['Gender_Encoded'] = df['Gender'].map(gender_map).fillna(-2) # Use -2 for any unmapped values (e.g., NaN or other strings)
    else:
        print("Warning: 'Gender' column missing in DataFrame for prepare_features.")
        df['Gender_Encoded'] = -1 # Placeholder if column is missing

    # Blood Type mapping
    if 'Blood Type' in df.columns:
        blood_map = {'A+':1,'A-':2,'B+':3,'B-':4,'AB+':5,'AB-':6,'O+':7,'O-':8}
        # Handle potential missing blood types by mapping them to a default or NaN, then fill
        df['Blood_Type_Encoded'] = df['Blood Type'].map(blood_map).fillna(0) # Map missing blood types to 0
    else:
        print("Warning: 'Blood Type' column missing in DataFrame for prepare_features.")
        df['Blood_Type_Encoded'] = 0 # Placeholder

    # Admission Type mapping
    if 'Admission Type' in df.columns:
        admission_map = {'Elective':0,'Urgent':1,'Emergency':2}
        df['Admission_Type_Encoded'] = df['Admission Type'].map(admission_map).fillna(-1) # Map missing to -1
    else:
        print("Warning: 'Admission Type' column missing in DataFrame for prepare_features.")
        df['Admission_Type_Encoded'] = -1 # Placeholder

    # Medication encoding (for treatment task)
    if task == "treatment":
        if 'Medication' in df.columns:
            le_med = LabelEncoder()
            # Fit on the entire column to ensure correct encoding and avoid uninitialized classes_ error
            df['Medication_Encoded'] = le_med.fit_transform(df['Medication'].astype(str))
        else:
            print("Warning: 'Medication' column missing for treatment task.")
            df['Medication_Encoded'] = -1 # Placeholder

    # Test Results encoding (for treatment task)
    if task == "treatment":
        if 'Test Results' in df.columns:
             # Map test results directly or use LabelEncoder
             test_result_map = {'Normal': 1, 'Inconclusive': 0, 'Abnormal': 0} # Example mapping
             df['Test_Result_Flag'] = df['Test Results'].map(test_result_map).fillna(0) # Default to 0 if missing or unknown
        else:
            print("Warning: 'Test Results' column missing for treatment task.")
            df['Test_Result_Flag'] = 0 # Placeholder

    # --- Define Features ---
    # Select features available AT ADMISSION
    features = [
        'Age', 'Gender_Encoded', 'Blood_Type_Encoded', 
        'Billing Amount', 'Admission_Type_Encoded'
    ]
    
    # Add task-specific features
    if task == "treatment":
        features.append('Medication_Encoded')
        features.append('Test_Result_Flag') # Test_Result_Flag is actually a target for treatment, but needed for X
    elif task == "high_billing":
        # High Billing task does not require additional features beyond the common set
        pass
    elif task == "length_of_stay":
        # Length of Stay task does not require additional features
        pass
    else:
        raise ValueError("Unknown task specified for prepare_features")

    # Filter DataFrame to only include required features, handling missing ones with default values (e.g., 0 or NaN)
    X = df.reindex(columns=features, fill_value=0) # Use 0 as a safe default, adjust if NaN is preferred

    # --- Define Targets ---
    y = None # Initialize y to None
    if task == "high_billing":
        if 'Billing Amount' in df.columns:
            # Threshold for high billing might need adjustment based on data analysis
            threshold = 30000 
            df['High_Billing'] = df['Billing Amount'].apply(lambda x: 1 if x > threshold else 0)
            y = df['High_Billing']
        else:
            print("Warning: 'Billing Amount' missing for high_billing task.")
            df['High_Billing'] = 0
            y = df['High_Billing']
            
    elif task == "treatment":
        if all(col in df.columns for col in ['Test Results', 'Hospital_Stay_Days', 'Billing Amount']):
            # Professional Logic: Success = Normal Test AND Stay <= 10 days AND Billing < 40,000
            # This makes the target "harder" and more realistic to predict
            df['Treatment_Success'] = (
                (df['Test Results'] == 'Normal') & 
                (df['Hospital_Stay_Days'] <= 10) & 
                (df['Billing Amount'] < 40000)
            ).astype(int)
            y = df['Treatment_Success']
        else:
            # Fallback if stay/billing columns aren't available during prediction
            test_result_map = {'Normal': 1, 'Inconclusive': 0, 'Abnormal': 0} 
            y = df['Test Results'].map(test_result_map).fillna(0)

    elif task == "length_of_stay":
        if 'Hospital_Stay_Days' in df.columns:
            y = df['Hospital_Stay_Days']  # Regression target
        else:
            print("Warning: 'Hospital_Stay_Days' missing for length_of_stay task target.")
            df['Hospital_Stay_Days'] = 0 # Placeholder
            y = df['Hospital_Stay_Days']
    
    # Ensure y is not None if a task was specified
    if y is None:
        raise ValueError(f"Target variable 'y' could not be determined for task: {task}")

    return X, y
