import logging
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from member1.run_ETL import run_pipeline

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

import subprocess
import sys

def scheduled_job():
    try:
        logging.info("🕒 Scheduled ETL & Report Generation started")
        # Step 1: Run ETL only (Updates DB with new data)
        # We use -m member1.run_ETL to run the module
        subprocess.run([sys.executable, "-m", "member1.run_ETL"], check=True)
        
        # Step 2: Generate Report (Updates the JSON for the dashboard)
        # We pass the main file or you could pass a specific chunk if using automation_runner
        subprocess.run([sys.executable, "member1/generate_report.py", "data/raw/healthcare.csv"], check=True)
        
        logging.info("✅ Data and Reports updated successfully")
    except Exception as e:
        logging.error(f"❌ Scheduled job failed: {e}")


# Schedule the job: every 60 seconds for demo/simulation
# In production, this would be daily: scheduler.add_job(scheduled_job, 'cron', hour=2)
scheduler.add_job(scheduled_job, 'interval', seconds=60)

if __name__ == "__main__":
    print("🚀 Scheduler active - running every 60 seconds...")
    logging.info("Scheduler started")
    # Run once immediately on start
    scheduled_job()
    scheduler.start()
