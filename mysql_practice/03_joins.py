"""
Querying Multiple Tables with JOIN
- INNER JOIN, LEFT JOIN, etc.
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
        SELECT e.first_name, e.last_name, d.department_name
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        LIMIT 5;
        '''
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
