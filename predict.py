import pandas as pd
import joblib
import os
from member3.feature_engineering import prepare_features

def test_predictions():
    # Load data
    processed_data = "data/processed/clean_data.csv"
    if not os.path.exists(processed_data):
        print(f"❌ Processed data not found at {processed_data}. Run 'python3 main.py' first.")
        return

    df = pd.read_csv(processed_data)
    
    # Pick a sample row (e.g., first row)
    sample_row = df.iloc[[2]]
    print("--- 🔬 Sample Patient for Prediction ---")
    print(sample_row[['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition', 'Admission Type']].to_string(index=False))
    print("-" * 40)

    # 1. Test High Billing Risk
    model_hb = joblib.load("member3_ml/models/high_billing_model.pkl")
    X_hb, y_hb = prepare_features(sample_row, "high_billing")
    pred_hb = model_hb.predict(X_hb)[0]
    print(f"💰 High Billing Risk Prediction: {'YES (Risk)' if pred_hb == 1 else 'NO (Safe)'}")

    # 2. Test Treatment Success
    model_tr = joblib.load("member3_ml/models/treatment_success_model.pkl")
    X_tr, y_tr = prepare_features(sample_row, "treatment")
    pred_tr = model_tr.predict(X_tr)[0]
    print(f"💊 Treatment Success (Normal Test Result): {'SUCCESS' if pred_tr == 1 else 'FAILURE'}")

    # 3. Test Length of Stay
    model_ls = joblib.load("member3_ml/models/length_of_stay_model.pkl")
    X_ls, y_ls = prepare_features(sample_row, "length_of_stay")
    pred_ls = model_ls.predict(X_ls)[0]
    print(f"🏥 Predicted Hospital Stay: {pred_ls:.1f} days (Actual: {sample_row['Hospital_Stay_Days'].values[0]} days)")

if __name__ == "__main__":
    test_predictions()
