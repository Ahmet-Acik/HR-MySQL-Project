"""
Programming with pandas (Variables, control flow, functions)
- Simulate stored procedures and control flow using Python functions
- pandas does not support SQL stored procedures, but Python is more flexible
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

def get_employee_count():
    """
    Simulates a stored procedure to count employees.
    What: Return the number of employees.
    Why: Encapsulate logic for reuse.
    How: Use a Python function.
    """
    employees = load_df('employees')
    return len(employees)

def employees_in_department(dept_id):
    """
    Simulates a parameterized stored procedure.
    What: Return employees in a given department.
    Why: Encapsulate logic with parameters.
    How: Use a Python function with arguments.
    """
    employees = load_df('employees')
    return employees[employees['department_id'] == dept_id]

def print_employee_summary():
    """
    Demonstrates control flow and function calls.
    """
    print(f"Total employees: {get_employee_count()}")
    for dept_id in [1, 2, 3]:
        df = employees_in_department(dept_id)
        print(f"Department {dept_id}: {len(df)} employees")

if __name__ == "__main__":
    print_employee_summary()
