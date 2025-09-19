"""
Using Functions and Aggregating Data (MySQL)
- COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING, multi-column grouping, percent-of-total, top-N per group, custom aggregations

Each block includes what, why, and how comments.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.db_config import HOST, USER, PASSWORD, DATABASE
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )


def print_query(cursor, query, params=None, label=None):
    if label:
        print(f"\n{label}")
    cursor.execute(query, params or ())
    for row in cursor.fetchall():
        print(row)

if __name__ == "__main__":
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        # 1. Basic GROUP BY: Count and average salary per department
        # What: Group employees by department, count them, and calculate average salary.
        # Why: Understand department sizes and pay levels.
        # How: GROUP BY + COUNT/AVG
        print_query(cursor,
            '''SELECT department_id, COUNT(*) AS num_employees, AVG(salary) AS avg_salary
               FROM employees GROUP BY department_id''',
            label="1. Group by department_id: count, avg salary")

        # 2. Sum of salaries by department
        # What: Total salary cost per department.
        # Why: Budgeting and cost analysis.
        print_query(cursor,
            '''SELECT department_id, SUM(salary) AS total_salary
               FROM employees GROUP BY department_id''',
            label="2. Sum of salaries by department:")

        # 3. Min/Max salary by department
        # What: Find salary range in each department.
        # Why: Identify pay gaps or outliers.
        print_query(cursor,
            '''SELECT department_id, MIN(salary) AS min_salary, MAX(salary) AS max_salary
               FROM employees GROUP BY department_id''',
            label="3. Min/Max salary by department:")

        # 4. Overall salary stats
        # What: Company-wide salary statistics.
        # Why: Executive summary.
        print_query(cursor,
            '''SELECT COUNT(*) AS num_employees, SUM(salary) AS total_salary, AVG(salary) AS avg_salary, MIN(salary) AS min_salary, MAX(salary) AS max_salary
               FROM employees''',
            label="4. Overall stats:")

        # 5. Multiple aggregations at once
        # What: All key stats per department.
        # Why: Dashboard-style summary.
        print_query(cursor,
            '''SELECT department_id, COUNT(*) AS num_employees, SUM(salary) AS total_salary, AVG(salary) AS avg_salary, MIN(salary) AS min_salary, MAX(salary) AS max_salary
               FROM employees GROUP BY department_id''',
            label="5. Multiple aggregations:")

        # 6. Aggregation with filtering (HAVING equivalent)
        # What: Departments with more than 5 employees.
        # Why: Focus on larger teams.
        # How: HAVING clause
        print_query(cursor,
            '''SELECT department_id, COUNT(*) AS num_employees
               FROM employees GROUP BY department_id HAVING COUNT(*) > 5''',
            label="6. Departments with more than 5 employees:")

        # 7. Aggregation by multiple columns (e.g., department and job)
        # What: Count employees by department and job.
        # Why: See job distribution within departments.
        print_query(cursor,
            '''SELECT department_id, job_id, COUNT(*) AS num_employees
               FROM employees GROUP BY department_id, job_id''',
            label="7. Count by department and job:")

        # 8. Percent of total (window function style)
        # What: Each department's share of total salary.
        # Why: Identify high-cost departments.
        print_query(cursor,
            '''SELECT department_id, SUM(salary) AS dept_salary,
                      ROUND(100 * SUM(salary) / (SELECT SUM(salary) FROM employees), 2) AS percent_of_total
               FROM employees GROUP BY department_id''',
            label="8. Percent of total salary by department:")

        # 9. Top N salaries per department (advanced: rank/partition)
        # What: Top 2 earners in each department.
        # Why: Find key/highest-paid staff per team.
        print_query(cursor,
            '''SELECT e.* FROM (
                   SELECT *, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
                   FROM employees
               ) e WHERE e.rnk <= 2
               ORDER BY department_id, rnk''',
            label="9. Top 2 salaries per department:")

        # 10. Custom aggregation (e.g., salary range)
        # What: Range = max - min salary per department.
        # Why: See pay spread.
        print_query(cursor,
            '''SELECT department_id, MAX(salary) - MIN(salary) AS salary_range
               FROM employees GROUP BY department_id''',
            label="10. Salary range per department:")
