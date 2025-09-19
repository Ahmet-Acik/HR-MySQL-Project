"""
Introduction to pandas with MySQL data
- How to load data from MySQL into pandas
- Basic DataFrame exploration
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
        df = pd.read_sql('SELECT * FROM employees', conn)
    return df

if __name__ == "__main__":
    df = load_employees_df()
    print(df.head())
    print(df.info())
