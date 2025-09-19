"""
Error Handling and Transactions
- Using try/except in Python
- MySQL transaction control (COMMIT, ROLLBACK)
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.db_config import HOST, USER, PASSWORD, DATABASE
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

if __name__ == "__main__":
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("START TRANSACTION;")
        cursor.execute("UPDATE employees SET salary = salary * 1.1 WHERE department_id = 10;")
        raise Exception("Simulated error: rolling back!")
        conn.commit()
    except Exception as e:
        print(f"Error occurred: {e}. Rolling back.")
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
