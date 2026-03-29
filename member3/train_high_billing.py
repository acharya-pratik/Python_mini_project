import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import joblib
from member3.feature_engineering import prepare_features

# Load processed data
df = pd.read_csv("data/processed/clean_data.csv")
X, y = prepare_features(df, task="high_billing")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"✅ High Billing Risk - Accuracy: {acc:.2f}, F1: {f1:.2f}")

joblib.dump(model, "member3_ml/models/high_billing_model.pkl")
print("✅ High Billing Risk model saved")
