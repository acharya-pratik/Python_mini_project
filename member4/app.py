import streamlit as st
import pandas as pd
import os
import sys

# Add the project root to sys.path so it can find 'config', 'member3', etc.
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path) 

from member4.db import load_data
from member4.predict import predict_patient_data, make_predictions 
import member4.visuals as visuals

st.set_page_config(layout="wide")
st.title("🏥 Healthcare Analytics Dashboard")

# Load data for existing tabs
try:
    df_all_data = load_data()
    df_all_data = make_predictions(df_all_data) 
except Exception as e:
    st.error(f"Error loading data or making predictions for dashboard: {e}")
    st.stop()


# ---------------- KPIs ----------------
st.subheader("📊 Key Metrics (Overall Data)")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", len(df_all_data))
col2.metric("Avg Billing", round(df_all_data['Billing Amount'].mean(),2))
col3.metric("Avg Stay Days", round(df_all_data['Hospital_Stay_Days'].mean(),2))
col4.metric("High Risk Patients", df_all_data['High_Billing_Pred'].sum())


# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Insights",
    "💰 High Billing Risk",
    "💊 Treatment Success",
    "🛏️ Length of Stay",
    "✨ Predict New Patient"
])

# ---------------- TAB 1: Insights ----------------
with tab1:
    st.subheader("General Insights & Distributions")

    col_viz1, col_viz2 = st.columns(2)
    with col_viz1:
        st.plotly_chart(visuals.age_distribution(df_all_data), use_container_width=True)
        st.plotly_chart(visuals.condition_pie(df_all_data), use_container_width=True)
    with col_viz2:
        st.plotly_chart(visuals.billing_by_condition(df_all_data), use_container_width=True)
        st.plotly_chart(visuals.stay_distribution(df_all_data), use_container_width=True)

    st.subheader("ML Model Performance Insights")
    st.plotly_chart(visuals.predicted_stay_distribution(df_all_data), use_container_width=True)
    st.plotly_chart(visuals.high_billing_prediction_distribution(df_all_data), use_container_width=True)


# ---------------- TAB 2: High Billing Risk ----------------
with tab2:
    st.subheader("High Billing Risk Analysis")

    risky_patients = df_all_data[df_all_data['High_Billing_Pred'] == 1]
    safe_patients = df_all_data[df_all_data['High_Billing_Pred'] == 0]

    risk_rate = len(risky_patients) / len(df_all_data) if len(df_all_data) > 0 else 0
    st.metric("High Risk Patients", len(risky_patients), f"{risk_rate:.1%}")

    st.dataframe(risky_patients[['Name','Medical Condition','Billing Amount','High_Billing_Pred']].sort_values('Billing Amount', ascending=False))

# ---------------- TAB 3: Treatment Success ----------------
with tab3:
    st.subheader("Treatment Success Analysis")

    success_rate = df_all_data['Treatment_Success_Pred'].mean()
    st.metric("Overall Treatment Success Rate", f"{success_rate:.1%}")

    st.dataframe(df_all_data[['Name','Medical Condition','Medication','Test Results','Treatment_Success_Pred']])

# ---------------- TAB 4: Length of Stay ----------------
with tab4:
    st.subheader("Length of Stay Prediction Analysis")

    avg_predicted_stay = df_all_data['Predicted_Stay'].mean()
    st.metric("Avg Predicted Hospital Stay", f"{avg_predicted_stay:.1f} days")

    st.dataframe(df_all_data[['Name','Medical Condition','Hospital_Stay_Days','Predicted_Stay']])

# ---------------- TAB 5: Predict New Patient ----------------
with tab5:
    st.subheader("Predict for a New Patient")
    st.write("Enter necessary patient details to get ML predictions.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        patient_name = col1.text_input("Patient Name", "John Doe")
        age = col2.number_input("Age", min_value=0, max_value=120, value=30)
        
        gender = col1.selectbox("Gender", ["Male", "Female"])
        blood_type = col2.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        billing_amount = col1.number_input("Billing Amount", min_value=0.0, value=15000.0)
        admission_type = col2.selectbox("Admission Type", ["Elective", "Urgent", "Emergency"])
        
        admission_date = col1.date_input("Date of Admission")

        medication = col2.selectbox("Medication", ["Paracetamol", "Ibuprofen", "Aspirin", "Penicillin", "Lipitor"])
        test_results = st.selectbox("Test Results (Current)", ["Normal", "Inconclusive", "Abnormal"])

        submitted = st.form_submit_button("Get Predictions")

        if submitted:
            # Create DataFrame for prediction
            patient_data = {
                'Name': [patient_name],
                'Age': [age],
                'Gender': [gender],
                'Blood Type': [blood_type],
                'Billing Amount': [billing_amount],
                'Admission Type': [admission_type],
                'Date of Admission': [admission_date],
                'Medication': [medication],
                'Test Results': [test_results]
            }
            
            pred_df = pd.DataFrame(patient_data)

            try:
                # Get predictions
                predictions = predict_patient_data(pred_df)

                if "error" in predictions:
                    st.error(predictions["error"])
                else:
                    st.write("--- Prediction Results ---")
                    col_res1, col_res2, col_res3 = st.columns(3)
                    col_res1.metric("High Billing Risk", predictions["High Billing Risk"])
                    col_res2.metric("Treatment Success", predictions["Treatment Success"])
                    col_res3.metric("Predicted Stay", f"{predictions['Predicted Length of Stay (days)']} days")

            except Exception as e:
                st.error(f"An unexpected error occurred during prediction: {e}")


st.success("✅ Dashboard Running!")
