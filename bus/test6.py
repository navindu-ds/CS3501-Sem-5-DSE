import mysql.connector

def clear_predictions_tables():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "ch1965298th",
        "database": "bus"
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    tables_to_clear = ["bus_run_time_predictions", "bus_dwell_time_predictions"]

    for table in tables_to_clear:
        query = f"DELETE FROM {table}"
        cursor.execute(query)
        conn.commit()
        print(f"Cleared data from {table} table.")

    cursor.close()
    conn.close()
