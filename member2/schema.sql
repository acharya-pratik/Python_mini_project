CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    blood_type VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS admissions (
    admission_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    admission_date DATE,
    discharge_date DATE,
    admission_type VARCHAR(50),
    hospital VARCHAR(100),
    doctor VARCHAR(100),
    medical_condition VARCHAR(100),
    medication VARCHAR(100),
    test_results VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    amount FLOAT,
    insurance_provider VARCHAR(100),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
