CREATE DATABASE IF NOT EXISTS healthcare_db;
USE healthcare_db;

-- 1. Dimension Tables (Lookups)
-- Added Composite Unique constraint to Patients to distinguish same names
CREATE TABLE Patients (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Age INT,
    Gender VARCHAR(50),
    BloodType VARCHAR(10),
    CONSTRAINT unique_patient_identity UNIQUE (Name, Age, Gender, BloodType)
);

CREATE TABLE Doctors (
    DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    DoctorName VARCHAR(255) UNIQUE
);

CREATE TABLE Hospitals (
    HospitalID INT AUTO_INCREMENT PRIMARY KEY,
    HospitalName VARCHAR(255) UNIQUE
);

CREATE TABLE MedicalConditions (
    ConditionID INT AUTO_INCREMENT PRIMARY KEY,
    ConditionName VARCHAR(255) UNIQUE
);

CREATE TABLE InsuranceProviders (
    InsuranceID INT AUTO_INCREMENT PRIMARY KEY,
    InsuranceName VARCHAR(255) UNIQUE
);

CREATE TABLE Medications (
    MedicationID INT AUTO_INCREMENT PRIMARY KEY,
    MedicationName VARCHAR(255) UNIQUE
);

-- 2. Fact Table (The Central Hub)
-- Added ON DELETE CASCADE and ON UPDATE CASCADE to all Foreign Keys
-- Added UNIQUE constraint to prevent duplicate Admission records
CREATE TABLE Admissions (
    AdmissionID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    HospitalID INT,
    ConditionID INT,
    InsuranceID INT,
    MedicationID INT,
    AdmissionDate DATE,
    DischargeDate DATE,
    RoomNumber INT,
    AdmissionType VARCHAR(50),
    BillingAmount DECIMAL(15, 2),
    TestResults VARCHAR(50),
    
    -- Foreign Keys with Cascading
    CONSTRAINT fk_patient FOREIGN KEY (PatientID) 
        REFERENCES Patients(PatientID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_doctor FOREIGN KEY (DoctorID) 
        REFERENCES Doctors(DoctorID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hospital FOREIGN KEY (HospitalID) 
        REFERENCES Hospitals(HospitalID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_condition FOREIGN KEY (ConditionID) 
        REFERENCES MedicalConditions(ConditionID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_insurance FOREIGN KEY (InsuranceID) 
        REFERENCES InsuranceProviders(InsuranceID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_medication FOREIGN KEY (MedicationID) 
        REFERENCES Medications(MedicationID) ON DELETE CASCADE ON UPDATE CASCADE,
        
    -- Uniqueness: Prevents the same stay from being logged twice
    CONSTRAINT unique_admission_stay UNIQUE (PatientID, AdmissionDate, RoomNumber)
);