# 📊 Folder: member4/ (Dashboard & User Interface)

### 📄 `app.py`
- **What it does:** The main Streamlit dashboard. It has tabs for Data Insights, AI Predictions, and Manual Patient entry.
- **Reason:** Provides a non-technical user interface for hospital administrators and doctors.

### 📄 `db.py`
- **What it does:** Connects the dashboard to MySQL.
- **Reason:** Enables real-time visualization of data as it's processed.

### 📄 `predict.py`
- **What it does:** Loads the trained `.pkl` models from the `member3_ml` folder and feeds them new data for predictions.
- **Reason:** The "Live Prediction Engine" of the user interface.

### 📄 `visuals.py`
- **What it does:** Creates Plotly charts (histograms, pie charts, etc.) using clean data.
- **Reason:** Keeps `app.py` focused on the UI by moving graphing logic here.
