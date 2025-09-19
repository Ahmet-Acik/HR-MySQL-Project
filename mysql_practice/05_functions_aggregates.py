"""
Using Functions and Aggregating Data
- COUNT, SUM, AVG, MIN, MAX, GROUP BY
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
        query = 'SELECT department_id, COUNT(*) as num_employees, AVG(salary) as avg_salary FROM employees GROUP BY department_id;'
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
