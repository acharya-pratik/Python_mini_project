# 🏥 Healthcare Data Engineering & ML Pipeline

This project is an end-to-end healthcare analytics system. It automates the journey from raw patient CSV data to a live, interactive dashboard with Machine Learning predictions.

## 📁 Project Structure Overview

- **`config/`**: System-wide settings (Database connections, Environment variables).
- **`member1/`**: ETL (Extract, Transform, Load) logic. The "Data Factory" of the project.
- **`member2/`**: Database administration and Pipeline Automation (Scheduling).
- **`member3/`**: Machine Learning Engineering. Features, Training, and Evaluation.
- **`member4/`**: User Interface. The Streamlit dashboard and prediction engine.
- **`data/`**: Storage for raw and processed datasets.
- **`member3_ml/models/`**: Storage for trained `.pkl` model files.
- **`logs/`**: Historical record of every pipeline run and error.

---

## 🚀 Execution Guide (What does what?)

### 1. The Full Pipeline (`python3 main.py`)
**Running this does:**
- Orchestrates the entire system in order.
- **ETL**: Cleans the CSV and populates the MySQL database.
- **ML Training**: Trains 3 separate models (Billing, Treatment, Stay).
- **Validation**: Verifies that the models are accurate before saving.
**Use this:** When you have new data or want to reset the system.

### 2. The Dashboard (`streamlit run member4/app.py`)
**Running this does:**
- Launches the web interface.
- Pulls live data from MySQL.
- Loads the trained models to give real-time predictions for new patients.
**Use this:** To visualize insights and interact with the AI.

### 3. The Scheduler (`python3 -m member2.scheduler`)
**Running this does:**
- Starts a background "Watchman."
- Every day (or interval), it automatically triggers the ETL to check for new data.
**Use this:** In production to keep the database and models up to date without manual work.
