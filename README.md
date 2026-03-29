# 🏥 Healthcare Data Engineering & ML Pipeline

This project is an end-to-end healthcare analytics system designed for professional-grade data ingestion, automated simulation, and predictive insights.

## 📁 Project Structure Overview

- **`config/`**: System-wide settings (Database connections, Environment variables).
- **`member1/`**: ETL (Extract, Transform, Load) logic and Live Report Generation.
- **`member2/`**: Database administration, Schema design, and Automation Scheduling.
- **`member3/`**: Machine Learning Engineering. Focus: High Billing Risk and Length of Stay.
- **`member4/`**: User Interface. Optimized Streamlit dashboard with real-time AI insights.
- **`data/simulation/`**: Automated data chunks for the live demo.
- **`member3_ml/models/`**: Storage for trained `.pkl` model files.

---

## 🚀 Execution Guide (Docker Optimized)

### 1. The Live Demo (Dashboard + Automation)
**Command:** `docker compose up`
- **What happens:** 
    - Starts the MySQL database.
    - Launches the **Automation Runner** in the background (ingests 250 new patients every 60s).
    - Starts the **Streamlit Dashboard** on `http://localhost:8501`.
- **Use this:** For the main presentation to show real-time data ingestion and instant AI analysis.

### 2. The Trainer (Total Data Learning)
**Command:** `docker compose run --rm train`
- **What happens:** 
    - Extracts the **total accumulated data** from the SQL database.
    - Trains two models: **High Billing Risk** (Classification) and **Length of Stay** (Regression).
    - Evaluates performance and saves the optimized `.pkl` files.
- **Use this:** Whenever you want the AI to learn from the new data added by the simulator.

---

## 📊 Dashboard Insights

- **📈 Latest Data Analysis**: Visualizes only the most recent 250 records processed by the automation loop. Shows "Direct Analysis" using pre-trained models.
- **💰 High Billing Risk**: Identifies patients with potential billing over $30k based on admission data (Age, Condition, etc.).
- **🛏️ Length of Stay**: Predicts hospital stay duration in days using admission-time features.
- **✨ Predict New Patient**: Interactive form to get real-time predictions for a custom patient profile.

## 🛠️ Optimization Highlights
- **Idempotent ETL**: Prevents data duplication even if tasks are repeated.
- **Dual-Layer Caching**: Historical data is cached for 5 mins; live chunks refresh every 10 seconds for a "snappy" UI.
- **Data Leakage Fix**: Models now strictly use features available *at admission* for realistic predictions.
