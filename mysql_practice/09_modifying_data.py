"""
Modifying Data (INSERT, UPDATE, DELETE)
- Best practices for DML
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
        cursor = conn.cursor()
        # Example: Insert
        cursor.execute("INSERT INTO departments (department_name, location_id) VALUES ('Test Dept', 1700);")
        conn.commit()
        print("Inserted new department.")
        # Example: Update
        cursor.execute("UPDATE departments SET department_name='Updated Dept' WHERE department_name='Test Dept';")
        conn.commit()
        print("Updated department.")
        # Example: Delete
        cursor.execute("DELETE FROM departments WHERE department_name='Updated Dept';")
        conn.commit()
        print("Deleted department.")
