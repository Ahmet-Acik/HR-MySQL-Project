"""
Programming with Transact-SQL (T-SQL) in MySQL
- Variables, control flow, stored procedures (MySQL style)
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
    with get_connection() as conn:
        cursor = conn.cursor()
        # Example: Create and call a stored procedure
        cursor.execute("""
        DROP PROCEDURE IF EXISTS get_employee_count;
        """)
        cursor.execute("""
        CREATE PROCEDURE get_employee_count()
        BEGIN
            SELECT COUNT(*) FROM employees;
        END;
        """)
        cursor.callproc('get_employee_count')
        for result in cursor.stored_results():
            print(result.fetchall())
