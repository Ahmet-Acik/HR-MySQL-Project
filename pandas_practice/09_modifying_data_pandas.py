"""
Modifying Data in pandas (INSERT, UPDATE, DELETE equivalents)
- Best practices for DataFrame mutation
- Note: pandas changes are in-memory unless written back to a database or file
"""
import sys
import os
import pandas as pd
import mysql.connector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.db_config import HOST, USER, PASSWORD, DATABASE

def get_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

def load_df(table):
    with get_connection() as conn:
        return pd.read_sql(f'SELECT * FROM {table}', conn)

def modifying_data_examples():
    """
    Demonstrates SQL DML (INSERT, UPDATE, DELETE) equivalents in pandas.
    Each block includes what, why, and how comments.
    """
    departments = load_df('departments')
    print("Original departments:")
    print(departments.tail())

    # 1. INSERT equivalent: Add a new row
    # What: Add a new department.
    # Why: Simulate data entry.
    new_row = {'department_id': departments['department_id'].max() + 1,
               'department_name': 'Test Dept',
               'manager_id': None,
               'location_id': 1700}
    departments = pd.concat([departments, pd.DataFrame([new_row])], ignore_index=True)
    print("\n1. After INSERT (add row):")
    print(departments.tail())

    # 2. UPDATE equivalent: Change department name
    # What: Update department name for 'Test Dept'.
    # Why: Simulate data correction.
    departments.loc[departments['department_name'] == 'Test Dept', 'department_name'] = 'Updated Dept'
    print("\n2. After UPDATE (change name):")
    print(departments.tail())

    # 3. DELETE equivalent: Remove the test department
    # What: Delete the row with department_name 'Updated Dept'.
    # Why: Simulate data cleanup.
    departments = departments[departments['department_name'] != 'Updated Dept']
    print("\n3. After DELETE (remove row):")
    print(departments.tail())

    # 4. Bulk UPDATE: Set all location_id=9999 for departments with id > 200
    # What: Bulk update location_id for certain departments.
    # Why: Simulate mass data change.
    departments.loc[departments['department_id'] > 200, 'location_id'] = 9999
    print("\n4. After bulk UPDATE (location_id):")
    print(departments.tail())

    # 5. Revert changes (reset to original)
    # What: Reload from DB to discard in-memory changes.
    # Why: Demonstrate that pandas changes are not persistent unless saved.
    departments = load_df('departments')
    print("\n5. After reload (revert changes):")
    print(departments.tail())

if __name__ == "__main__":
    modifying_data_examples()
