from config.db_config import get_connection

def load_data(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        # Insert into patients
        cursor.execute("""
            INSERT INTO patients (name, age, gender, blood_type)
            VALUES (%s, %s, %s, %s)
        """, (row['Name'], row['Age'], row['Gender'], row['Blood Type']))

        patient_id = cursor.lastrowid

        # Insert into admissions
        cursor.execute("""
            INSERT INTO admissions (
                patient_id, admission_date, discharge_date,
                admission_type, hospital, doctor,
                medical_condition, medication, test_results
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            patient_id,
            row['Date of Admission'],
            row['Discharge Date'],
            row['Admission Type'],
            row['Hospital'],
            row['Doctor'],
            row['Medical Condition'],
            row['Medication'],
            row['Test Results']
        ))

        # Insert into billing
        cursor.execute("""
            INSERT INTO billing (
                patient_id, amount, insurance_provider
            )
            VALUES (%s, %s, %s)
        """, (
            patient_id,
            row['Billing Amount'],
            row['Insurance Provider']
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Data loaded into MySQL!")
