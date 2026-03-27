import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# --- CONFIGURATION ---
USER = "root"
PASSWORD = "rAmram12#@123"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "healthcare_db"

encoded_pass = quote_plus(PASSWORD)
DATABASE_URL = f"mysql+mysqlconnector://{USER}:{encoded_pass}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

# --- SECTION 1: ETL LOGIC (Data Ingestion) ---

def preprocess_dimensions(df):
    """Syncs unique names from CSV into Dimension tables."""
    dim_configs = [
        ('Doctor', 'Doctors', 'DoctorName'),
        ('Hospital', 'Hospitals', 'HospitalName'),
        ('Medical Condition', 'MedicalConditions', 'ConditionName'),
        ('Insurance Provider', 'InsuranceProviders', 'InsuranceName'),
        ('Medication', 'Medications', 'MedicationName')
    ]
    
    with engine.begin() as conn:
        for csv_col, db_table, db_col in dim_configs:
            unique_vals = [{"v": val} for val in df[csv_col].unique() if pd.notnull(val)]
            if unique_vals:
                conn.execute(text(f"INSERT IGNORE INTO {db_table} ({db_col}) VALUES (:v)"), unique_vals)
        
        # Batch Patient Update
        patients = df[['Name', 'Age', 'Gender', 'Blood Type']].drop_duplicates().dropna()
        patient_data = [{"n": r['Name'], "a": r['Age'], "g": r['Gender'], "bt": r['Blood Type']} for _, r in patients.iterrows()]
        if patient_data:
            conn.execute(text("INSERT IGNORE INTO Patients (Name, Age, Gender, BloodType) VALUES (:n, :a, :g, :bt)"), patient_data)

def get_dimension_maps():
    """Loads DB IDs into dictionaries for fast lookup."""
    maps = {}
    with engine.connect() as conn:
        maps['Doctor'] = {r.DoctorName: r.DoctorID for r in conn.execute(text("SELECT DoctorID, DoctorName FROM Doctors"))}
        maps['Hospital'] = {r.HospitalName: r.HospitalID for r in conn.execute(text("SELECT HospitalID, HospitalName FROM Hospitals"))}
        maps['Condition'] = {r.ConditionName: r.ConditionID for r in conn.execute(text("SELECT ConditionID, ConditionName FROM MedicalConditions"))}
        maps['Insurance'] = {r.InsuranceName: r.InsuranceID for r in conn.execute(text("SELECT InsuranceID, InsuranceName FROM InsuranceProviders"))}
        maps['Medication'] = {r.MedicationName: r.MedicationID for r in conn.execute(text("SELECT MedicationID, MedicationName FROM Medications"))}
        maps['Patient'] = {(r.Name, r.Age, r.Gender, r.BloodType): r.PatientID for r in conn.execute(text("SELECT PatientID, Name, Age, Gender, BloodType FROM Patients"))}
    return maps

def run_etl_process(file_path="healthcare_dataset.csv"):
    print(f"\n[1/2] Starting ETL Process: {datetime.now().strftime('%H:%M:%S')}")
    try:
        reader = pd.read_csv(file_path, chunksize=5000)
        for chunk in reader:
            preprocess_dimensions(chunk)
            dim_maps = get_dimension_maps()
            
            # Map CSV columns to Database IDs
            chunk['pid'] = chunk.apply(lambda x: dim_maps['Patient'].get((x['Name'], x['Age'], x['Gender'], x['Blood Type'])), axis=1)
            chunk['did'] = chunk['Doctor'].map(dim_maps['Doctor'])
            chunk['hid'] = chunk['Hospital'].map(dim_maps['Hospital'])
            chunk['cid'] = chunk['Medical Condition'].map(dim_maps['Condition'])
            chunk['iid'] = chunk['Insurance Provider'].map(dim_maps['Insurance'])
            chunk['mid'] = chunk['Medication'].map(dim_maps['Medication'])

            valid_rows = chunk.dropna(subset=['pid', 'did', 'hid'])
            insert_list = [{
                "pid": r['pid'], "did": r['did'], "hid": r['hid'], "cid": r['cid'],
                "iid": r['iid'], "mid": r['mid'], "adate": r['Date of Admission'],
                "ddate": r['Discharge Date'], "room": r['Room Number'],
                "atype": r['Admission Type'], "bill": r['Billing Amount'], "test": r['Test Results']
            } for _, r in valid_rows.iterrows()]

            if insert_list:
                with engine.begin() as conn:
                    conn.execute(text("""
                        INSERT IGNORE INTO Admissions 
                        (PatientID, DoctorID, HospitalID, ConditionID, InsuranceID, MedicationID, 
                         AdmissionDate, DischargeDate, RoomNumber, AdmissionType, BillingAmount, TestResults)
                        VALUES (:pid, :did, :hid, :cid, :iid, :mid, :adate, :ddate, :room, :atype, :bill, :test)
                    """), insert_list)
        print("ETL Sync Completed Successfully.")
    except Exception as e:
        print(f"ETL Error: {e}")

# --- SECTION 2: ANALYTICS LOGIC (Data Reporting) ---

def run_analytics_report():
    print(f"\n[2/2] Generating Analytics Report: {datetime.now().strftime('%H:%M:%S')}")
    try:
        with engine.connect() as connection:
            # 1. Monthly Trends
            print("\n--- Monthly Admissions ---")
            trend_q = text("SELECT DATE_FORMAT(AdmissionDate, '%Y-%m') AS month, COUNT(*) AS total FROM Admissions GROUP BY month ORDER BY month DESC LIMIT 6")
            for row in connection.execute(trend_q):
                print(f"Month: {row.month} | Admissions: {row.total}")

            # 2. Avg Billing by Condition (Using the normalized join)
            print("\n--- Avg Billing by Medical Condition ---")
            bill_q = text("""
                SELECT c.ConditionName, ROUND(AVG(a.BillingAmount), 2) AS avg_bill 
                FROM Admissions a 
                JOIN MedicalConditions c ON a.ConditionID = c.ConditionID 
                GROUP BY c.ConditionName
            """)
            for row in connection.execute(bill_q):
                print(f"{row.ConditionName}: ${row.avg_bill}")

            # 3. Efficiency: Length of Stay (LOS)
            print("\n--- Average Stay (Days) by Hospital ---")
            los_q = text("""
                SELECT h.HospitalName, ROUND(AVG(DATEDIFF(a.DischargeDate, a.AdmissionDate)), 1) AS avg_stay 
                FROM Admissions a 
                JOIN Hospitals h ON a.HospitalID = h.HospitalID 
                GROUP BY h.HospitalName
            """)
            for row in connection.execute(los_q):
                print(f"{row.HospitalName}: {row.avg_stay} days")
    except Exception as e:
        print(f"Analytics Error: {e}")

# --- SECTION 3: SCHEDULER ---

def daily_pipeline():
    run_etl_process()
    run_analytics_report()

scheduler = BlockingScheduler()
# Runs every day at midnight
scheduler.add_job(daily_pipeline, 'cron', hour=0, minute=0)

if __name__ == "__main__":
    print("Hospital Data Pipeline Active.")
    # Run once immediately to verify everything works
    daily_pipeline()
    # scheduler.start() # Uncomment to keep running as a background service