import joblib
import pandas as pd
import streamlit as st
from member3.feature_engineering import prepare_features

# Load models
try:
    hb_model = joblib.load("member3_ml/models/high_billing_model.pkl")
    ls_model = joblib.load("member3_ml/models/length_of_stay_model.pkl")
except FileNotFoundError as e:
    st.error(f"Error loading ML models: {e}. Please ensure 'python3 main.py' has been run to train models.")
    st.stop()

def make_predictions(df):
    try:
        # --- High Billing Prediction ---
        X_hb, _ = prepare_features(df, task="high_billing")
        df['High_Billing_Pred'] = hb_model.predict(X_hb)

        # --- Length of Stay Prediction ---
        X_ls, _ = prepare_features(df, task="length_of_stay")
        df['Predicted_Stay'] = ls_model.predict(X_ls)
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        return df

    return df

def predict_patient_data(patient_data_df):
    try:
        # High Billing Prediction
        X_hb, _ = prepare_features(patient_data_df, task="high_billing")
        pred_hb = hb_model.predict(X_hb)[0]
        pred_hb_label = "YES (Risk)" if pred_hb == 1 else "NO (Safe)"

        # Length of Stay Prediction
        X_ls, _ = prepare_features(patient_data_df, task="length_of_stay")
        pred_ls = ls_model.predict(X_ls)[0]

        return {
            "High Billing Risk": pred_hb_label,
            "Predicted Length of Stay (days)": round(pred_ls, 1)
        }
    except Exception as e:
        return {"error": f"An error occurred during prediction: {e}"}
