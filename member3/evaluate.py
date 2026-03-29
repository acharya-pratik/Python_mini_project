import pandas as pd
import joblib
from member3.feature_engineering import prepare_features
from sklearn.metrics import classification_report, mean_squared_error, r2_score, root_mean_squared_error

df = pd.read_csv("data/processed/clean_data.csv")

# High Billing
model_hb = joblib.load("member3_ml/models/high_billing_model.pkl")
X_hb, y_hb = prepare_features(df, "high_billing")
y_pred_hb = model_hb.predict(X_hb)
print("✅ High Billing Classification Report")
print(classification_report(y_hb, y_pred_hb))

# Treatment Success
model_tr = joblib.load("member3_ml/models/treatment_success_model.pkl")
X_tr, y_tr = prepare_features(df, "treatment")
y_pred_tr = model_tr.predict(X_tr)
print("✅ Treatment Success Classification Report")
print(classification_report(y_tr, y_pred_tr))

# Length of Stay
model_ls = joblib.load("member3_ml/models/length_of_stay_model.pkl")
X_ls, y_ls = prepare_features(df, "length_of_stay")
y_pred_ls = model_ls.predict(X_ls)
rmse = root_mean_squared_error(y_ls, y_pred_ls)
r2 = r2_score(y_ls, y_pred_ls)
print(f"✅ Length of Stay - RMSE: {rmse:.2f}, R2: {r2:.2f}")
