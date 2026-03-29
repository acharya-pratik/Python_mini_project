import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, root_mean_squared_error
import joblib
from member3.feature_engineering import prepare_features

df = pd.read_csv("data/processed/clean_data.csv")
X, y = prepare_features(df, task="length_of_stay")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Length of Stay - RMSE: {rmse:.2f}, R2: {r2:.2f}")

joblib.dump(model, "member3_ml/models/length_of_stay_model.pkl")
print("✅ Length of Stay model saved")
