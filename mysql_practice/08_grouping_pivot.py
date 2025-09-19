"""
Grouping Sets and Pivoting Data
- MySQL supports GROUPING SETS (from 8.0.18+), but not PIVOT directly
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
        query = '''
        SELECT department_id, job_id, COUNT(*) as num_employees
        FROM employees
        GROUP BY department_id, job_id WITH ROLLUP;
        '''
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
