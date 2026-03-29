from apscheduler.schedulers.blocking import BlockingScheduler
from member1.run_ETL import run_pipeline
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

scheduler = BlockingScheduler()

def scheduled_job():
    try:
        logging.info("Pipeline started")
        run_pipeline()
        logging.info("Pipeline finished successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

# Schedule the job: daily at 2am
scheduler.add_job(scheduled_job, 'cron', hour=2, minute=0)

if __name__ == "__main__":
    logging.info("Scheduler started")
    scheduler.start()
