import streamlit as st
import pandas as pd
import os
import sys
import warnings

# Add the project root to sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path) 

from member4.db import load_data
from member4.predict import predict_patient_data, make_predictions 
import member4.visuals as visuals

# ---------------- Dashboard Configuration ----------------
st.set_page_config(layout="wide", page_title="Healthcare Analytics")
st.title("🏥 Healthcare Analytics Dashboard")

# ---------------- Optimized Data Loading ----------------

@st.cache_data(ttl=10) # Very short cache for the latest chunk (live demo)
def get_latest_batch():
    latest_chunk_path = "data/simulation/latest_chunk.csv"
    if os.path.exists(latest_chunk_path):
        df_latest = pd.read_csv(latest_chunk_path)
        # Fast conversion
        df_latest['Date of Admission'] = pd.to_datetime(df_latest['Date of Admission'])
        df_latest['Discharge Date'] = pd.to_datetime(df_latest['Discharge Date'])
        df_latest['Hospital_Stay_Days'] = (df_latest['Discharge Date'] - df_latest['Date of Admission']).dt.days
        # Only predict on these 250 rows (Instant)
        df_latest = make_predictions(df_latest)
        return df_latest
    return None

@st.cache_data(ttl=300) # Long cache for historical data (5 minutes)
def get_historical_data():
    df = load_data()
    # Predicting on 50,000+ rows is slow, so we cache the result
    df = make_predictions(df)
    return df

# Background load historical data
df_all_data = get_historical_data()
# Fast load latest batch
df_latest = get_latest_batch()

# ---------------- Live Simulation Header ----------------
def load_simulation_report():
    report_path = "data/simulation/latest_report.json"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            import json
            return json.load(f)
    return None

sim_report = load_simulation_report()

if sim_report:
    st.info(f"🛰️ Live Simulation Active | Last Update: {sim_report['last_updated']}")
    
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        st.markdown("#### 📦 Latest Chunk (250 rows)")
        c1, c2, c3 = st.columns(3)
        c1.metric("Count", sim_report['recent']['count'])
        c2.metric("Avg Billing", f"${sim_report['recent']['avg_billing']:,.0f}")
        c3.metric("Top Condition", sim_report['recent']['most_common_condition'])
        
        if 'ml_insights' in sim_report['recent']:
            ml = sim_report['recent']['ml_insights']
            st.markdown("---")
            st.markdown("**🤖 Real-time AI Analysis**")
            m1, m2 = st.columns(2)
            m1.metric("High Risk Patients", ml['high_risk_count'])
            m2.metric("Avg Pred Stay", f"{ml['avg_predicted_stay']:.1f}d")
        
    with col_sim2:
        st.markdown("#### 🌍 Running Total (Database)")
        t1, t2, t3 = st.columns(3)
        t1.metric("Total Patients", f"{sim_report['total']['count']:,}")
        t2.metric("Total Avg Billing", f"${sim_report['total']['avg_billing']:,.0f}")
        t3.metric("Total Top Condition", sim_report['total']['most_common_condition'])
    
    st.divider()

# ---------------- Main Metrics ----------------
st.subheader("📊 Key Metrics (Overall Data)")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Total Patients", f"{len(df_all_data):,}")
col_m2.metric("Avg Billing", f"${df_all_data['Billing Amount'].mean():,.2f}")
col_m3.metric("Avg Stay Days", f"{df_all_data['Hospital_Stay_Days'].mean():.1f}")
col_m4.metric("Total High Risk (Pred)", f"{df_all_data['High_Billing_Pred'].sum():,}")

# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Latest Data Analysis",
    "💰 High Billing Risk",
    "🛏️ Length of Stay",
    "✨ Predict New Patient"
])

# Use the fast df_latest for Tab 1
with tab1:
    display_df = df_latest if df_latest is not None else df_all_data.tail(250)
    st.subheader(f"Insights for the Latest Batch")

    col_viz1, col_viz2 = st.columns(2)
    with col_viz1:
        st.plotly_chart(visuals.age_distribution(display_df), use_container_width=True)
        st.plotly_chart(visuals.condition_pie(display_df), use_container_width=True)
    with col_viz2:
        st.plotly_chart(visuals.billing_by_condition(display_df), use_container_width=True)
        st.plotly_chart(visuals.stay_distribution(display_df), use_container_width=True)

# Tabs 2 & 3 use cached historical data
with tab2:
    st.subheader("High Billing Risk Analysis")
    risky_patients = df_all_data[df_all_data['High_Billing_Pred'] == 1].head(100)
    st.dataframe(risky_patients[['Name','Medical Condition','Billing Amount','High_Billing_Pred']])

with tab3:
    st.subheader("Length of Stay Prediction Analysis")
    st.dataframe(df_all_data[['Name','Medical Condition','Hospital_Stay_Days','Predicted_Stay']].head(100))

with tab4:
    st.subheader("Predict for a New Patient")
    with st.form("prediction_form"):
        c1, c2 = st.columns(2)
        patient_name = c1.text_input("Patient Name", "John Doe")
        age = c2.number_input("Age", 0, 120, 30)
        gender = c1.selectbox("Gender", ["Male", "Female"])
        blood_type = c2.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        billing_amount = c1.number_input("Billing Amount", 0.0, 100000.0, 15000.0)
        admission_type = c2.selectbox("Admission Type", ["Elective", "Urgent", "Emergency"])
        med_cond = c1.selectbox("Medical Condition", ["Cancer", "Obesity", "Diabetes", "Asthma", "Hypertension", "Arthritis"])
        
        submitted = st.form_submit_button("Get Predictions")
        if submitted:
            patient_data = {
                'Name': [patient_name], 'Age': [age], 'Gender': [gender],
                'Blood Type': [blood_type], 'Billing Amount': [billing_amount],
                'Admission Type': [admission_type], 'Medical Condition': [med_cond],
                'Date of Admission': [pd.Timestamp.now()], 'Discharge Date': [pd.Timestamp.now()]
            }
            res = predict_patient_data(pd.DataFrame(patient_data))
            st.write(res)

st.success("✅ Dashboard Optimized!")
