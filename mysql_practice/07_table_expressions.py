"""
Using Table Expressions (CTE, Derived Tables)
- MySQL supports CTEs (WITH ...)
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
        WITH high_salary AS (
            SELECT * FROM employees WHERE salary > 10000
        )
        SELECT * FROM high_salary;
        '''
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
