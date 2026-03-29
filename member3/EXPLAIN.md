# 🤖 Folder: member3/ (Machine Learning Engineering)

### 📄 `feature_engineering.py`
- **What it does:** Converts categorical strings (like "Gender") to numbers (0/1). It also creates the **Treatment Success** target using complex medical logic.
- **Reason:** Machine Learning models can only "read" numbers. This file is the "Translator."

### 📄 `train_high_billing.py`
- **What it does:** Trains a Random Forest to predict if a patient will incur more than $30,000 in costs.
- **Reason:** Helps hospitals prepare for high-cost cases.

### 📄 `train_treatment.py`
- **What it does:** Trains a model to predict the success of a treatment plan.
- **Reason:** Clinical decision support for doctors.

### 📄 `train_length_of_stay.py`
- **What it does:** Uses Regression to estimate how many days a patient will stay in the hospital.
- **Reason:** Critical for bed management and hospital resources.

### 📄 `evaluate.py`
- **What it does:** Tests the models against data they haven't seen before and prints Accuracy/RMSE.
- **Reason:** To prove the models are trustworthy before being used in the dashboard.
