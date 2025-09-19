"""
Set operations using pandas
- union, intersection, difference
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

def load_employees_departments():
    with get_connection() as conn:
        employees = pd.read_sql('SELECT first_name FROM employees', conn)
        departments = pd.read_sql('SELECT department_name FROM departments', conn)
    return employees, departments

def set_operator_examples():
    employees, departments = load_employees_departments()
    # UNION
    union = pd.concat([employees.rename(columns={'first_name': 'name'}), departments.rename(columns={'department_name': 'name'})]).drop_duplicates().reset_index(drop=True)
    print("UNION:")
    print(union.head())
    # UNION ALL
    union_all = pd.concat([employees.rename(columns={'first_name': 'name'}), departments.rename(columns={'department_name': 'name'})]).reset_index(drop=True)
    print("\nUNION ALL:")
    print(union_all.head())
    # INTERSECT
    intersect = pd.merge(employees.rename(columns={'first_name': 'name'}), departments.rename(columns={'department_name': 'name'}), on='name')
    print("\nINTERSECT:")
    print(intersect.head())
    # EXCEPT
    except_df = employees[~employees['first_name'].isin(departments['department_name'])]
    print("\nEXCEPT:")
    print(except_df.head())

if __name__ == "__main__":
    set_operator_examples()
