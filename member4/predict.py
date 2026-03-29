import joblib
import pandas as pd
import streamlit as st
from member3.feature_engineering import prepare_features # Ensure this is correctly imported

# Load models
try:
    hb_model = joblib.load("member3_ml/models/high_billing_model.pkl")
    tr_model = joblib.load("member3_ml/models/treatment_success_model.pkl")
    ls_model = joblib.load("member3_ml/models/length_of_stay_model.pkl")
except FileNotFoundError as e:
    st.error(f"Error loading ML models: {e}. Please ensure 'python3 main.py' has been run to train models.")
    st.stop()

# Keep make_predictions for dashboard usage to add predictions to historical data
def make_predictions(df):
    # Ensure required columns are present for feature engineering
    # These are columns that are expected by prepare_features but might not be in the DB query results directly
    # For example, if some data was missing in raw CSV and dropped
    # Or if the DB schema is different from raw/processed.
    # We will rely on the DB query in member4/db.py to provide necessary columns.

    # If columns are missing from the loaded DF, prepare_features will raise an error.
    # We need to ensure that prepare_features can handle potential NaNs or missing values gracefully,
    # or that the data loading step ensures all required columns are present.

    try:
        # --- High Billing Prediction ---
        X_hb, _ = prepare_features(df, task="high_billing")
        df['High_Billing_Pred'] = hb_model.predict(X_hb)

        # --- Treatment Success Prediction ---
        X_tr, _ = prepare_features(df, task="treatment")
        df['Treatment_Success_Pred'] = tr_model.predict(X_tr)

        # --- Length of Stay Prediction ---
        X_ls, _ = prepare_features(df, task="length_of_stay")
        df['Predicted_Stay'] = ls_model.predict(X_ls)
    except KeyError as e:
        st.error(f"Missing column for prediction: {e}. Ensure all necessary columns are loaded from the database.")
        # Optionally, return df with original columns or raise error to stop
        return df # Return original df if prediction fails
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        return df

    return df


def predict_patient_data(patient_data_df):
    """
    Predicts outcomes for a single patient's data.
    Takes a single-row DataFrame as input.
    """
    try:
        # High Billing Prediction
        X_hb, _ = prepare_features(patient_data_df, task="high_billing")
        pred_hb = hb_model.predict(X_hb)[0]
        pred_hb_label = "YES (Risk)" if pred_hb == 1 else "NO (Safe)"

        # Treatment Success Prediction
        X_tr, _ = prepare_features(patient_data_df, task="treatment")
        pred_tr = tr_model.predict(X_tr)[0]
        pred_tr_label = "SUCCESS" if pred_tr == 1 else "FAILURE"

        # Length of Stay Prediction
        X_ls, _ = prepare_features(patient_data_df, task="length_of_stay")
        pred_ls = ls_model.predict(X_ls)[0]

        return {
            "High Billing Risk": pred_hb_label,
            "Treatment Success": pred_tr_label,
            "Predicted Length of Stay (days)": round(pred_ls, 1)
        }
    except KeyError as e:
        return {"error": f"Missing data for prediction: {e}. Please ensure all required fields are provided."}
    except Exception as e:
        return {"error": f"An error occurred during prediction: {e}"}
