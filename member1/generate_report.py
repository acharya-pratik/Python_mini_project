import os
import sys

# Add project root to sys.path BEFORE any local imports
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

import pandas as pd
import json
import joblib
from config.db_config import get_connection
from member3.feature_engineering import prepare_features

def generate_report(recent_chunk_file, output_file="data/simulation/latest_report.json"):
    # Load recent chunk
    df_recent = pd.read_csv(recent_chunk_file)
    
    # --- ML Analysis on the New Chunk ---
    ml_insights = {
        "high_risk_count": 0,
        "avg_predicted_stay": 0.0
    }

    try:
        # Load existing models
        # Ensure paths are correct relative to project root
        hb_model = joblib.load("member3_ml/models/high_billing_model.pkl")
        ls_model = joblib.load("member3_ml/models/length_of_stay_model.pkl")

        # 1. High Billing Risk
        X_hb, _ = prepare_features(df_recent, task="high_billing")
        preds_hb = hb_model.predict(X_hb)
        ml_insights["high_risk_count"] = int(sum(preds_hb))

        # 2. Length of Stay
        X_ls, _ = prepare_features(df_recent, task="length_of_stay")
        preds_ls = ls_model.predict(X_ls)
        ml_insights["avg_predicted_stay"] = float(round(preds_ls.mean(), 1))

    except Exception as e:
        print(f"⚠️ ML Prediction skipped during report generation: {e}")

    # Simple recent stats
    recent_stats = {
        "count": len(df_recent),
        "avg_billing": float(round(df_recent['Billing Amount'].mean(), 2)),
        "most_common_condition": df_recent['Medical Condition'].mode()[0] if not df_recent.empty else "N/A",
        "ml_insights": ml_insights
    }
    
    # DB stats (Total)
    try:
        conn = get_connection()
        cursor = conn.cursor(buffered=True)
        
        cursor.execute("SELECT COUNT(*) FROM admissions")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(amount) FROM billing")
        total_avg_billing = cursor.fetchone()[0]
        
        cursor.execute("SELECT medical_condition, COUNT(*) as c FROM admissions GROUP BY medical_condition ORDER BY c DESC LIMIT 1")
        res = cursor.fetchone()
        total_most_common_condition = res[0] if res else "N/A"
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error querying DB: {e}")
        total_count, total_avg_billing, total_most_common_condition = 0, 0, "Error"
    
    total_stats = {
        "count": total_count,
        "avg_billing": float(round(total_avg_billing, 2)) if total_avg_billing else 0.0,
        "most_common_condition": total_most_common_condition
    }
    
    # Save the chunk itself for the dashboard to use in detailed plots
    df_recent.to_csv("data/simulation/latest_chunk.csv", index=False)

    report = {
        "recent": recent_stats,
        "total": total_stats,
        "last_updated": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(report, f, indent=4)
    
    print(f"📊 Report updated at {report['last_updated']} with ML Insights")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_report(sys.argv[1])
    else:
        print("Usage: python3 member1/generate_report.py <chunk_csv>")
