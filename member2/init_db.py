from config.db_config import get_connection

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
