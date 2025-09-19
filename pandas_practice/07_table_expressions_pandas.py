"""
Using Table Expressions in pandas
- CTE (WITH), derived tables, and subquery equivalents
- pandas does not have CTEs, but you can simulate them with intermediate DataFrames
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

def table_expression_examples():
    """
    Demonstrates SQL table expressions (CTE, derived tables) in pandas.
    Each block includes what, why, and how comments.
    """
    employees = load_df('employees')
    # 1. Derived table: Employees with salary > 10000
    # What: Filter employees with high salary.
    # Why: Focus on high earners.
    # How: Assign filtered DataFrame to a variable (like a derived table)
    high_salary = employees[employees['salary'] > 10000]
    print("1. Employees with salary > 10000 (derived table):")
    print(high_salary)

    # 2. CTE-like: Use intermediate DataFrame for further analysis
    # What: Employees with salary > 10000, then count by department
    # Why: See which departments have high earners.
    # How: Use the previous DataFrame as input to groupby
    high_salary_by_dept = high_salary.groupby('department_id').size().reset_index(name='num_high_earners')
    print("\n2. High salary count by department (CTE-like):")
    print(high_salary_by_dept)

    # 3. Nested derived tables: Top 3 earners per department
    # What: For each department, get top 3 salaries.
    # Why: Identify top earners per team.
    # How: Use groupby + rank, then filter
    employees['rank'] = employees.groupby('department_id')['salary'].rank(method='first', ascending=False)
    top3 = employees[employees['rank'] <= 3].sort_values(['department_id', 'rank'])
    print("\n3. Top 3 earners per department (nested derived table):")
    print(top3[['employee_id', 'department_id', 'salary', 'rank']])

    # 4. Multi-step CTE-like: Chain multiple intermediate results
    # What: Employees with salary > 5000, then those in departments with >5 such employees
    # Why: Find large, well-paid teams.
    high_paid = employees[employees['salary'] > 5000]
    dept_counts = high_paid['department_id'].value_counts()
    large_depts = dept_counts[dept_counts > 5].index
    result = high_paid[high_paid['department_id'].isin(large_depts)]
    print("\n4. Employees with salary > 5000 in large departments (multi-step CTE-like):")
    print(result)

    # 5. Inline view: Use a DataFrame as a subquery in a merge
    # What: Join high_salary with departments info
    # Why: Add department names to high earners
    departments = load_df('departments')
    merged = pd.merge(high_salary, departments, on='department_id', how='left')
    print("\n5. High salary employees with department info (inline view):")
    print(merged.head())

if __name__ == "__main__":
    table_expression_examples()
