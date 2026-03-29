# 🏭 Folder: member1/ (ETL - Data Engineering)

### 📄 `extract.py`
- **What it does:** Reads raw data from `data/raw/healthcare.csv`.
- **Reason:** Isolation of input sources. If you later change to an API, you only change this file.

### 📄 `validate.py`
- **What it does:** Checks data for quality (Nulls, negative ages, invalid dates).
- **Reason:** Prevents "Garbage In, Garbage Out." It stops the pipeline if the data is corrupted.

### 📄 `transform.py`
- **What it does:** Cleans text (Title Case names), converts date formats, and handles duplicates.
- **Reason:** Standardizes the data so the database and ML models can process it consistently.

### 📄 `add_feature.py`
- **What it does:** Calculates "Stay Days" and "Long Stay" flags.
- **Reason:** Creates the "Targets" that the Machine Learning models will learn to predict.

### 📄 `load.py`
- **What it does:** Inserts the cleaned data into MySQL tables.
- **Reason:** Moves data from temporary CSV files into a structured, relational database for fast querying by the dashboard.

### 📄 `run_ETL.py`
- **What it does:** The main script that calls all of the above in order.
- **Reason:** Provides a single entry point for the "Data Ingestion" phase.
