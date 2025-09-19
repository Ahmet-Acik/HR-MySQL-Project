"""
SELECT-like queries using pandas
- Filtering, selecting columns, sorting, etc.
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

def load_employees_df():
    with get_connection() as conn:
        return pd.read_sql('SELECT * FROM employees', conn)

def select_examples():
    df = load_employees_df()
    print("First 5 employees:")
    print(df.head())
    print("\nEmployees with salary > 5000:")
    print(df[df['salary'] > 5000])
    print("\nEmployee names:")
    print(df[['first_name', 'last_name']])
    print("\nEmployees in department 1:")
    print(df[df['department_id'] == 1])

if __name__ == "__main__":
    select_examples()
