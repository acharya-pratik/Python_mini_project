from config.db_config import get_connection

def load_data(df):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)

    for _, row in df.iterrows():

        # Check if patient already exists
        cursor.execute("""
            SELECT patient_id FROM patients 
            WHERE name = %s AND age = %s AND gender = %s
        """, (row['Name'], row['Age'], row['Gender']))
        
        res = cursor.fetchone()
        if res:
            patient_id = res[0]
        else:
            # Insert into patients
            cursor.execute("""
                INSERT INTO patients (name, age, gender, blood_type)
                VALUES (%s, %s, %s, %s)
            """, (row['Name'], row['Age'], row['Gender'], row['Blood Type']))
            patient_id = cursor.lastrowid

        # Check if admission already exists
        cursor.execute("""
            SELECT admission_id FROM admissions 
            WHERE patient_id = %s AND admission_date = %s AND hospital = %s
        """, (patient_id, row['Date of Admission'], row['Hospital']))
        
        res_adm = cursor.fetchone()
        if not res_adm:
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

        # Check if billing record already exists
        cursor.execute("""
            SELECT bill_id FROM billing 
            WHERE patient_id = %s AND amount = %s
        """, (patient_id, row['Billing Amount']))
        
        res_bill = cursor.fetchone()
        if not res_bill:
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
