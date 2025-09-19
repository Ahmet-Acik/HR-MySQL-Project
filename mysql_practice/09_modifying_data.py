"""
Modifying Data (INSERT, UPDATE, DELETE)
- Best practices for DML: transactions, error handling, bulk operations, and safe testing

Each block includes what, why, and how comments.
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


def print_departments(cursor, label=None):
    if label:
        print(f"\n{label}")
    cursor.execute("SELECT * FROM departments ORDER BY department_id DESC LIMIT 5;")
    for row in cursor.fetchall():
        print(row)

if __name__ == "__main__":
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # 1. INSERT: Add a new department
            # What: Add a new department.
            # Why: Simulate data entry.
            # How: Use parameterized query for safety
            cursor.execute("INSERT INTO departments (department_name, location_id) VALUES (%s, %s);", ('Test Dept', 1700))
            conn.commit()
            print_departments(cursor, label="1. After INSERT (add row):")

            # 2. UPDATE: Change department name
            # What: Update department name for 'Test Dept'.
            # Why: Simulate data correction.
            cursor.execute("UPDATE departments SET department_name=%s WHERE department_name=%s;", ('Updated Dept', 'Test Dept'))
            conn.commit()
            print_departments(cursor, label="2. After UPDATE (change name):")

            # 3. DELETE: Remove the test department
            # What: Delete the row with department_name 'Updated Dept'.
            # Why: Simulate data cleanup.
            cursor.execute("DELETE FROM departments WHERE department_name=%s;", ('Updated Dept',))
            conn.commit()
            print_departments(cursor, label="3. After DELETE (remove row):")

            # 4. Bulk UPDATE: Set all location_id=9999 for departments with id > 200
            # What: Bulk update location_id for certain departments.
            # Why: Simulate mass data change.
            cursor.execute("UPDATE departments SET location_id=9999 WHERE department_id > 200;")
            conn.commit()
            print_departments(cursor, label="4. After bulk UPDATE (location_id):")

            # 5. Revert changes (reset to original)
            # What: Rollback bulk update for demonstration (if possible)
            # Why: Show transaction/rollback (if autocommit off)
            # Note: Here, we reload the connection to discard in-memory changes, but in real DB, you must restore from backup or use transactions.
            # For demo, just print current state
            print_departments(cursor, label="5. Final state (no rollback in demo):")

    except Exception as e:
        print("Error during DML operations:", e)
