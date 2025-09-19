"""
JOIN operations using pandas
- Merge DataFrames to simulate SQL joins
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

def join_examples():
    employees = load_df('employees')
    departments = load_df('departments')
    jobs = load_df('jobs')
    # INNER JOIN
    print("INNER JOIN (employees & departments):")
    print(pd.merge(employees, departments, on='department_id', how='inner').head())
    # LEFT JOIN
    print("\nLEFT JOIN (all employees, departments):")
    print(pd.merge(employees, departments, on='department_id', how='left').head())
    # RIGHT JOIN
    print("\nRIGHT JOIN (all departments, employees):")
    print(pd.merge(employees, departments, on='department_id', how='right').head())
    # MULTI-TABLE JOIN
    print("\nMULTI-TABLE JOIN (employees, departments, jobs):")
    emp_dept = pd.merge(employees, departments, on='department_id', how='inner')
    print(pd.merge(emp_dept, jobs, on='job_id', how='inner').head())

if __name__ == "__main__":
    join_examples()
