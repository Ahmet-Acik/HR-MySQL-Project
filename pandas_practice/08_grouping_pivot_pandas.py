"""
Grouping Sets and Pivoting Data in pandas
- GROUP BY, ROLLUP, and pivot_table equivalents
- pandas supports flexible groupby and pivot_table operations
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

def grouping_pivot_examples():
    """
    Demonstrates SQL grouping sets, rollup, and pivoting in pandas.
    Each block includes what, why, and how comments.
    """
    employees = load_df('employees')
    # 1. Basic groupby: count employees by department and job
    # What: Count employees for each department/job combination.
    # Why: See job distribution per department.
    group = employees.groupby(['department_id', 'job_id']).size().reset_index(name='num_employees')
    print("1. Count employees by department and job:")
    print(group)

    # 2. ROLLUP equivalent: add subtotals by department and grand total
    # What: Add department totals and overall total.
    # Why: Summarize at multiple levels.
    rollup = employees.groupby(['department_id', 'job_id']).size().reset_index(name='num_employees')
    dept_totals = employees.groupby('department_id').size().reset_index(name='num_employees')
    dept_totals['job_id'] = 'ALL'
    grand_total = pd.DataFrame({'department_id': ['ALL'], 'job_id': ['ALL'], 'num_employees': [len(employees)]})
    rollup_all = pd.concat([rollup, dept_totals, grand_total], ignore_index=True)
    print("\n2. ROLLUP equivalent (subtotals and grand total):")
    print(rollup_all)

    # 3. Pivot table: departments as rows, jobs as columns
    # What: Pivot to see job counts per department in a matrix.
    # Why: Easier comparison across jobs/departments.
    pivot = employees.pivot_table(index='department_id', columns='job_id', values='employee_id', aggfunc='count', fill_value=0)
    print("\n3. Pivot table (departments as rows, jobs as columns):")
    print(pivot)

    # 4. Multi-level pivot: add gender (if exists) as another dimension
    # What: Pivot by department, job, and gender (if gender column exists).
    # Why: Analyze workforce diversity by role and department.
    if 'gender' in employees.columns:
        pivot_multi = employees.pivot_table(index=['department_id', 'gender'], columns='job_id', values='employee_id', aggfunc='count', fill_value=0)
        print("\n4. Multi-level pivot (with gender):")
        print(pivot_multi)
    else:
        print("\n4. Multi-level pivot (with gender): Gender column not found.")

    # 5. Unpivot (melt): convert pivoted data back to long format
    # What: Unpivot the previous pivot table.
    # Why: Prepare for further analysis or visualization.
    unpivot = pivot.reset_index().melt(id_vars='department_id', var_name='job_id', value_name='num_employees')
    print("\n5. Unpivot (melt) the pivot table:")
    print(unpivot.head())

if __name__ == "__main__":
    grouping_pivot_examples()
