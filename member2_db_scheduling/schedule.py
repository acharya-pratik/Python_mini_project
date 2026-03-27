import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# -------------------------------
# DATABASE CONFIGURATION
# -------------------------------
USER = "root"
PASSWORD = "rAmram12#@123"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "healthcare_db"

encoded_pass = quote_plus(PASSWORD)
DATABASE_URL = f"mysql+mysqlconnector://{USER}:{encoded_pass}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

# -------------------------------
# 1. LOAD DIMENSION MAPS
# -------------------------------
def get_dimension_maps():
    with engine.connect() as conn:
        return {
            "Doctor": {r.DoctorName: r.DoctorID for r in conn.execute(text("SELECT DoctorID, DoctorName FROM Doctors"))},
            "Hospital": {r.HospitalName: r.HospitalID for r in conn.execute(text("SELECT HospitalID, HospitalName FROM Hospitals"))},
            "Condition": {r.ConditionName: r.ConditionID for r in conn.execute(text("SELECT ConditionID, ConditionName FROM MedicalConditions"))},
            "Insurance": {r.InsuranceName: r.InsuranceID for r in conn.execute(text("SELECT InsuranceID, InsuranceName FROM InsuranceProviders"))},
            "Medication": {r.MedicationName: r.MedicationID for r in conn.execute(text("SELECT MedicationID, MedicationName FROM Medications"))},
            "Patient": {(r.Name, r.Age, r.Gender, r.BloodType): r.PatientID for r in conn.execute(
                text("SELECT PatientID, Name, Age, Gender, BloodType FROM Patients")
            )}
        }

# -------------------------------
# 2. DIMENSION INSERT 
# -------------------------------
def update_dimensions(df):
    dim_configs = [
        ("Doctor", "Doctors", "DoctorName"),
        ("Hospital", "Hospitals", "HospitalName"),
        ("Medical Condition", "MedicalConditions", "ConditionName"),
        ("Insurance Provider", "InsuranceProviders", "InsuranceName"),
        ("Medication", "Medications", "MedicationName")
    ]

    with engine.begin() as conn:
        for csv_col, table, col in dim_configs:
            values = [{"v": v} for v in df[csv_col]]
            conn.execute(
                text(f"INSERT IGNORE INTO {table} ({col}) VALUES (:v)"),
                values
            )

        # Patients
        patients = df[['Name', 'Age', 'Gender', 'Blood Type']]
        patient_rows = [
            {"n": r["Name"], "a": r["Age"], "g": r["Gender"], "bt": r["Blood Type"]}
            for _, r in patients.iterrows()
        ]

        conn.execute(
            text("""
                INSERT INTO Patients (Name, Age, Gender, BloodType)
                VALUES (:n, :a, :g, :bt)
            """),
            patient_rows
        )

# -------------------------------
# 3. MAIN LOADING (500 RECORDS/DAY)
# -------------------------------
def run_load_process(file_path="healthcare_dataset.csv"):
    print(f"\n[ETL START] {datetime.now()}")

    try:
        # Read only 500 rows per run
        df = pd.read_csv(file_path).head(500)

        # Step 1: Insert/update dimension tables
        update_dimensions(df)

        # Step 2: Load ID maps
        dim_maps = get_dimension_maps()

        # Step 3: Map IDs
        df["pid"] = df.apply(lambda x: dim_maps["Patient"].get(
            (x["Name"], x["Age"], x["Gender"], x["Blood Type"])
        ), axis=1)

        df["did"] = df["Doctor"].map(dim_maps["Doctor"])
        df["hid"] = df["Hospital"].map(dim_maps["Hospital"])
        df["cid"] = df["Medical Condition"].map(dim_maps["Condition"])
        df["iid"] = df["Insurance Provider"].map(dim_maps["Insurance"])
        df["mid"] = df["Medication"].map(dim_maps["Medication"])

        # Step 4: Prepare fact table inserts
        records = [
            {
                "pid": r["pid"],
                "did": r["did"],
                "hid": r["hid"],
                "cid": r["cid"],
                "iid": r["iid"],
                "mid": r["mid"],
                "adate": r["Date of Admission"],
                "ddate": r["Discharge Date"],
                "room": r["Room Number"],
                "atype": r["Admission Type"],
                "bill": r["Billing Amount"],
                "test": r["Test Results"]
            }
            for _, r in df.iterrows()
        ]

        # Step 5: Insert into fact table
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO Admissions
                    (PatientID, DoctorID, HospitalID, ConditionID,
                     InsuranceID, MedicationID, AdmissionDate,
                     DischargeDate, RoomNumber, AdmissionType,
                     BillingAmount, TestResults)
                    VALUES
                    (:pid, :did, :hid, :cid, :iid, :mid,
                     :adate, :ddate, :room, :atype, :bill, :test)
                """),
                records
            )

        print("[ETL SUCCESS] 500 records processed")

    except Exception as e:
        print(f"[ETL ERROR] {e}")

def daily_pipeline():
    run_load_process()
   

# -------------------------------
# SCHEDULER (RUN DAILY)
# -------------------------------
scheduler = BlockingScheduler()
scheduler.add_job(daily_pipeline, 'cron', hour=0, minute=0)

if __name__ == "__main__":
    print("Healthcare ETL Pipeline Started")
    
    # Run once immediately
    daily_pipeline()

    # Uncomment for continuous daily automation
    # scheduler.start()