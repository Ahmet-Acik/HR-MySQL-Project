"""
Error Handling and Transactions in pandas
- Using try/except in Python
- Simulate transaction-like logic (in-memory)
- pandas does not support DB transactions, but you can use context managers and error handling
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

def error_handling_transaction_examples():
    """
    Demonstrates error handling and transaction-like logic in pandas.
    Each block includes what, why, and how comments.
    """
    employees = load_df('employees')
    print("Original salaries (last 5):")
    print(employees[['employee_id', 'salary']].tail())

    # 1. Simulate transaction: try/except with in-memory copy
    # What: Try to update salaries, revert on error.
    # Why: Mimic DB transaction rollback.
    employees_copy = employees.copy()
    try:
        employees_copy.loc[employees_copy['department_id'] == 10, 'salary'] *= 1.1
        raise Exception("Simulated error: rolling back!")
    except Exception as e:
        print(f"\nError occurred: {e}. Rolling back changes.")
        employees_copy = employees.copy()  # Revert to original
    print("\nAfter simulated rollback (should match original):")
    print(employees_copy[['employee_id', 'salary']].tail())

    # 2. Commit: Only apply changes if no error
    # What: Only update if all is well.
    # Why: Mimic DB commit.
    employees_copy = employees.copy()
    try:
        employees_copy.loc[employees_copy['department_id'] == 10, 'salary'] *= 1.1
        # No error, so "commit"
        print("\nAfter commit (salaries updated):")
        print(employees_copy[['employee_id', 'salary']].tail())
    except Exception as e:
        print(f"Error: {e}")

    # 3. Error handling in data processing
    # What: Handle errors in data transformation.
    # Why: Robust data pipelines.
    try:
        employees['salary'] = employees['salary'].astype(float)
        employees['bonus'] = employees['bonus']  # This will fail if 'bonus' column doesn't exist
    except Exception as e:
        print(f"\nHandled data processing error: {e}")

if __name__ == "__main__":
    error_handling_transaction_examples()
