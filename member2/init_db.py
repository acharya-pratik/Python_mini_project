import os
import sys
from config.db_config import get_connection

# Add project root to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

def run_schema():
    conn = get_connection()
    cursor = conn.cursor()

    with open("member2/schema.sql", "r") as f:
        sql_script = f.read()

    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    run_schema()
