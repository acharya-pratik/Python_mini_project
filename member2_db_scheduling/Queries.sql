--- Monthly Admissions ---

SELECT DATE_FORMAT(AdmissionDate, '%Y-%m') AS month,
COUNT(*) AS total
FROM Admissions
GROUP BY month
ORDER BY month DESC
LIMIT 6;

--- Avg Billing by Condition ---
            
SELECT c.ConditionName,
ROUND(AVG(a.BillingAmount), 2) AS avg_bill
FROM Admissions a
JOIN MedicalConditions c ON a.ConditionID = c.ConditionID
GROUP BY c.ConditionName;

--- Avg Stay by Hospital ---
           
SELECT h.HospitalName,
ROUND(AVG(DATEDIFF(a.DischargeDate, a.AdmissionDate)), 1) AS avg_stay
FROM Admissions a
JOIN Hospitals h ON a.HospitalID = h.HospitalID
GROUP BY h.HospitalName