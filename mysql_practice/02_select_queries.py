"""
Querying Tables with SELECT
- Basic SELECT statements
- Filtering with WHERE
"""
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
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees LIMIT 5;")
        for row in cursor.fetchall():
            print(row)
