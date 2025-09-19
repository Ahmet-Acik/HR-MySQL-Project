"""
Using Subqueries and APPLY with pandas
- Scalar, correlated, and IN subquery equivalents
- MySQL does not support APPLY, but pandas can simulate similar logic
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

def subquery_examples():
    """
    Demonstrates SQL subquery patterns in pandas.
    Each block includes what, why, and how comments.
    """
    employees = load_df('employees')
    # 1. Scalar subquery: Employees with salary above company average
    # What: Find employees whose salary is above the average.
    # Why: Identify high earners.
    avg_salary = employees['salary'].mean()
    print("1. Employees with salary > company average:")
    print(employees[employees['salary'] > avg_salary])

    # 2. IN subquery: Employees in departments with more than 5 employees
    # What: Find employees in large departments.
    # Why: Focus on big teams.
    dept_counts = employees['department_id'].value_counts()
    large_depts = dept_counts[dept_counts > 5].index
    print("\n2. Employees in departments with >5 employees:")
    print(employees[employees['department_id'].isin(large_depts)])

    # 3. Correlated subquery: Employees earning more than department average
    # What: Find employees who earn more than their department's average.
    # Why: Spot top earners per department.
    dept_avg = employees.groupby('department_id')['salary'].transform('mean')
    print("\n3. Employees earning more than department average:")
    print(employees[employees['salary'] > dept_avg])

    # 4. EXISTS subquery: Employees in departments with at least one manager
    # What: Find employees in departments that have a manager.
    # Why: Filter for managed teams.
    # How: Simulate EXISTS with merge
    departments = load_df('departments')
    # Ensure job_id is string before using .str.contains
    job_id_str = employees['job_id'].astype(str)
    managers = employees[job_id_str.str.contains('MAN', na=False)]
    managed_depts = managers['department_id'].unique()
    print("\n4. Employees in departments with a manager:")
    print(employees[employees['department_id'].isin(managed_depts)])

    # 5. APPLY-like: Add department average salary as a column (window function style)
    # What: Annotate each employee with their department's average salary.
    # Why: For comparison and analytics.
    employees['dept_avg_salary'] = employees.groupby('department_id')['salary'].transform('mean')
    print("\n5. Employees with department average salary column:")
    print(employees[['employee_id', 'department_id', 'salary', 'dept_avg_salary']].head())

if __name__ == "__main__":
    subquery_examples()
