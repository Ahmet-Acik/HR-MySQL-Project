"""
Using Set Operators (UNION, INTERSECT, EXCEPT)
- MySQL supports UNION and UNION ALL
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
        cursor = conn.cursor(dictionary=True)
        query = '''
        SELECT first_name FROM employees
        UNION
        SELECT department_name FROM departments;
        '''
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
