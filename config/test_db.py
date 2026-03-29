import time
from config.db_config import get_connection

def test_connection():
    time.sleep(10)  # wait for MySQL

    try:
        conn = get_connection()
        print("✅ Connected to MySQL!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)

test_connection()
