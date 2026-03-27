import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# -------------------------------
# DATABASE CONFIG
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
# LOAD CSV INTO STAGING
# -------------------------------
def load_to_staging(file_path):
    print("Loading CSV into staging...")

    df = pd.read_csv(file_path).head(250)

    # Load into staging (replace every run)
    df.to_sql("staging_healthcare", con=engine, if_exists="replace", index=False)

    print(f"[INFO] {len(df)} rows loaded into staging")


# -------------------------------
# LOAD DIMENSIONS
# -------------------------------
def load_dimensions():
    print("Updating dimensions...")

    queries = [

        # Doctors
        """
        INSERT IGNORE INTO Doctors (DoctorName)
        SELECT DISTINCT Doctor FROM staging_healthcare
        """,

        # Hospitals
        """
        INSERT IGNORE INTO Hospitals (HospitalName)
        SELECT DISTINCT Hospital FROM staging_healthcare
        """,

        # Conditions
        """
        INSERT IGNORE INTO MedicalConditions (ConditionName)
        SELECT DISTINCT `Medical Condition` FROM staging_healthcare
        """,

        # Insurance
        """
        INSERT IGNORE INTO InsuranceProviders (InsuranceName)
        SELECT DISTINCT `Insurance Provider` FROM staging_healthcare
        """,

        # Medications
        """
        INSERT IGNORE INTO Medications (MedicationName)
        SELECT DISTINCT Medication FROM staging_healthcare
        """,

        # Patients 
        """
        INSERT IGNORE INTO Patients (Name, Age, Gender, BloodType)
        SELECT DISTINCT Name, Age, Gender, `Blood Type`
        FROM staging_healthcare
        """
    ]

    with engine.begin() as conn:
        for q in queries:
            conn.execute(text(q))

    print("[INFO] Dimensions updated")


# -------------------------------
# LOAD FACT TABLE
# -------------------------------
def load_fact():
    print("Loading fact table...")

    query = """
    INSERT IGNORE INTO Admissions (
        PatientID, DoctorID, HospitalID, ConditionID,
        InsuranceID, MedicationID, AdmissionDate,
        DischargeDate, RoomNumber, AdmissionType,
        BillingAmount, TestResults
    )
    SELECT 
        p.PatientID,
        d.DoctorID,
        h.HospitalID,
        c.ConditionID,
        i.InsuranceID,
        m.MedicationID,
        s.`Date of Admission`,
        s.`Discharge Date`,
        s.`Room Number`,
        s.`Admission Type`,
        s.`Billing Amount`,
        s.`Test Results`
    FROM staging_healthcare s
    JOIN Patients p ON p.Name = s.Name 
        AND p.Age = s.Age 
        AND p.Gender = s.Gender 
        AND p.BloodType = s.`Blood Type`
    JOIN Doctors d ON d.DoctorName = s.Doctor
    JOIN Hospitals h ON h.HospitalName = s.Hospital
    JOIN MedicalConditions c ON c.ConditionName = s.`Medical Condition`
    JOIN InsuranceProviders i ON i.InsuranceName = s.`Insurance Provider`
    JOIN Medications m ON m.MedicationName = s.Medication
    """

    with engine.begin() as conn:
        conn.execute(text(query))

    print("[INFO] Fact table loaded ")


# -------------------------------
# MAIN PIPELINE
# -------------------------------
def run_pipeline():
    print(f"\n[START] {datetime.now()}")

    try:
        load_to_staging("healthcare_dataset.csv")
        load_dimensions()
        load_fact()

        print("[ETL SUCCESS] Completed successfully")

    except Exception as e:
        print(f"[ETL ERROR] {e}")


# -------------------------------
# SCHEDULER 
# -------------------------------
def daily_job():
    run_pipeline()


scheduler = BlockingScheduler()
scheduler.add_job(daily_job, 'cron', hour=0, minute=0)

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print("Healthcare ETL Pipeline Started")

    # Run once
    run_pipeline()

    # Uncomment for daily automation
    # scheduler.start()