"""
Using Functions and Aggregating Data with pandas
- COUNT, SUM, AVG, MIN, MAX, GROUP BY equivalents
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

def aggregate_examples():
    """
    Demonstrates SQL-like aggregation and grouping in pandas.
    Each block includes what, why, and how comments.
    """
    df = load_employees_df()

    # 1. Basic GROUP BY: Count and average salary per department
    # What: Group employees by department, count them, and calculate average salary.
    # Why: Understand department sizes and pay levels.
    # How: groupby + agg
    print("1. Group by department_id: count, avg salary")
    print(df.groupby('department_id').agg(num_employees=('employee_id', 'count'), avg_salary=('salary', 'mean')))

    # 2. Sum of salaries by department
    # What: Total salary cost per department.
    # Why: Budgeting and cost analysis.
    print("\n2. Sum of salaries by department:")
    print(df.groupby('department_id')['salary'].sum())

    # 3. Min/Max salary by department
    # What: Find salary range in each department.
    # Why: Identify pay gaps or outliers.
    print("\n3. Min/Max salary by department:")
    print(df.groupby('department_id')['salary'].agg(['min', 'max']))

    # 4. Overall salary stats
    # What: Company-wide salary statistics.
    # Why: Executive summary.
    print("\n4. Overall stats:")
    print(df['salary'].agg(['count', 'sum', 'mean', 'min', 'max']))

    # 5. Multiple aggregations at once
    # What: All key stats per department.
    # Why: Dashboard-style summary.
    print("\n5. Multiple aggregations:")
    print(df.groupby('department_id').agg(
        num_employees=('employee_id', 'count'),
        total_salary=('salary', 'sum'),
        avg_salary=('salary', 'mean'),
        min_salary=('salary', 'min'),
        max_salary=('salary', 'max')
    ))

    # 6. Aggregation with filtering (HAVING equivalent)
    # What: Departments with more than 5 employees.
    # Why: Focus on larger teams.
    # How: Filter after groupby/agg
    print("\n6. Departments with more than 5 employees:")
    dept_stats = df.groupby('department_id').agg(num_employees=('employee_id', 'count'))
    print(dept_stats[dept_stats['num_employees'] > 5])

    # 7. Aggregation by multiple columns (e.g., department and job)
    # What: Count employees by department and job.
    # Why: See job distribution within departments.
    print("\n7. Count by department and job:")
    print(df.groupby(['department_id', 'job_id']).size().unstack(fill_value=0))

    # 8. Percent of total (window function style)
    # What: Each department's share of total salary.
    # Why: Identify high-cost departments.
    print("\n8. Percent of total salary by department:")
    salary_by_dept = df.groupby('department_id')['salary'].sum()
    percent = 100 * salary_by_dept / salary_by_dept.sum()
    print(percent)

    # 9. Top N salaries per department (advanced: rank/partition)
    # What: Top 2 earners in each department.
    # Why: Find key/highest-paid staff per team.
    print("\n9. Top 2 salaries per department:")
    df['rank'] = df.groupby('department_id')['salary'].rank(method='first', ascending=False)
    print(df[df['rank'] <= 2].sort_values(['department_id', 'rank']))

    # 10. Custom aggregation (e.g., salary range)
    # What: Range = max - min salary per department.
    # Why: See pay spread.
    print("\n10. Salary range per department:")
    print(df.groupby('department_id')['salary'].agg(salary_range=lambda x: x.max() - x.min()))

if __name__ == "__main__":
    aggregate_examples()
