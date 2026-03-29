import pandas as pd
from config.db_config import get_connection

def load_data():
    conn = get_connection()

    query = """
    SELECT 
        p.name AS Name,
        p.age AS Age,
        p.gender AS Gender,
        p.blood_type AS `Blood Type`,
        a.admission_date AS `Date of Admission`,
        a.discharge_date AS `Discharge Date`,
        a.admission_type AS `Admission Type`,
        a.hospital AS Hospital,
        a.doctor AS Doctor,
        a.medical_condition AS `Medical Condition`,
        a.medication AS Medication,
        a.test_results AS `Test Results`,
        b.amount AS `Billing Amount`,
        b.insurance_provider AS `Insurance Provider`
    FROM patients p
    JOIN admissions a ON p.patient_id = a.patient_id
    JOIN billing b ON p.patient_id = b.patient_id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    # Re-calculate Hospital_Stay_Days which is needed for ML
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    df['Hospital_Stay_Days'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
    
    # Calculate Long_Stay flag
    df['Long_Stay'] = df['Hospital_Stay_Days'].apply(lambda x: 1 if x > 7 else 0)

    return df
