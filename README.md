# Healthcare Data Pipeline Project

## Project Overview
An end-to-end healthcare data engineering and machine learning pipeline involving data collection, ETL, database management, predictive modeling, and dashboarding.

## Team Structure & Responsibilities

### [Member 1] Data Engineer (ETL)
**Folder:** `member1_etl/`
- **Goal:** Data collection and cleaning.
- **Tasks:** 
    - Download Kaggle dataset (prasad22).
    - Handle missing values and clean data types.
    - Load cleaned data into MySQL.
- **Deliverables:** `clean_data.csv`, ETL script.

### [Member 2] Database & Storage Architect
**Folder:** `member2_db_scheduling/`
- **Goal:** Schema design and automation.
- **Tasks:**
    - Design 3NF MySQL schema (Patients, Admissions, Billing).
    - Write analytical SQL queries.
    - Implement daily pipeline scheduling using `apscheduler`.
- **Deliverables:** `schema.sql`, `scheduler.py`.

### [Member 3] ML Engineer
**Folder:** `member3_ml/`
- **Goal:** Predictive modeling.
- **Tasks:**
    - Feature engineering (encoding gender, blood type).
    - Train Random Forest for medical condition/readmission risk.
    - Evaluate performance (F1, Accuracy, Feature Importance).
- **Deliverables:** `model_training.py`, `model_eval_report.md`.

### [Member 4] Dashboard & Reporting
**Folder:** `member4_dashboard/`
- **Goal:** Visualization and Monitoring.
- **Tasks:**
    - Build Streamlit dashboard.
    - Visualize patient flow and billing analytics.
    - Implement logging for pipeline runs and anomalies.
- **Deliverables:** `app.py`, `pipeline.log`.

## Workflow
1. **Member 1** performs ETL and populates MySQL.
2. **Member 2** structures the DB and sets up the auto-refresh.
3. **Member 3 & 4** pull from the shared database in parallel to build the model and dashboard.

## Branching Strategy
- `main`: Stable integration branch.
- `member1-etl`: ETL development.
- `member2-db`: Schema and scheduling development.
- `member3-ml`: ML model development.
- `member4-ui`: Dashboard development.
