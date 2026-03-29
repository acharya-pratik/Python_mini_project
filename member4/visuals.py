import plotly.express as px
import pandas as pd

def age_distribution(df):
    if df.empty: return px.bar()
    return px.histogram(df, x='Age', title="Age Distribution")

def billing_by_condition(df):
    if df.empty: return px.bar()
    data = df.groupby('Medical Condition')['Billing Amount'].mean().reset_index()
    return px.bar(data, x='Medical Condition', y='Billing Amount', title="Avg Billing by Condition")

def condition_pie(df):
    if df.empty: return px.pie()
    data = df['Medical Condition'].value_counts().reset_index()
    data.columns = ['Condition','Count']
    return px.pie(data, names='Condition', values='Count', title="Condition Distribution")

def stay_distribution(df):
    if df.empty: return px.histogram()
    return px.histogram(df, x='Hospital_Stay_Days', title="Hospital Stay Distribution")

# New graphs for prediction analysis
def predicted_stay_distribution(df):
    if df.empty or 'Predicted_Stay' not in df.columns: return px.histogram()
    return px.histogram(df, x='Predicted_Stay', title="Predicted Length of Stay Distribution")

def high_billing_prediction_distribution(df):
    if df.empty or 'High_Billing_Pred' not in df.columns: return px.bar()
    pred_counts = df['High_Billing_Pred'].map({0: 'Safe', 1: 'High Risk'}).value_counts().reset_index()
    pred_counts.columns = ['Prediction', 'Count']
    return px.bar(pred_counts, x='Prediction', y='Count', title="High Billing Prediction Distribution")
