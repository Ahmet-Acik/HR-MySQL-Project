"""
Using Subqueries and APPLY (MySQL does not support APPLY, but supports subqueries)
- Scalar, correlated, IN, and EXISTS subqueries
- APPLY-like logic using subqueries or joins

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

        # 1. Scalar subquery: Employees with salary above company average
        # What: Find employees whose salary is above the average.
        # Why: Identify high earners.
        # How: Scalar subquery in WHERE
        print_query(cursor,
            '''SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)''',
            label="1. Employees with salary > company average:")

        # 2. IN subquery: Employees in departments with more than 5 employees
        # What: Find employees in large departments.
        # Why: Focus on big teams.
        # How: IN subquery
        print_query(cursor,
            '''SELECT * FROM employees WHERE department_id IN (
                   SELECT department_id FROM employees GROUP BY department_id HAVING COUNT(*) > 5
               )''',
            label="2. Employees in departments with >5 employees:")

        # 3. Correlated subquery: Employees earning more than department average
        # What: Find employees who earn more than their department's average.
        # Why: Spot top earners per department.
        # How: Correlated subquery in WHERE
        print_query(cursor,
            '''SELECT * FROM employees e1 WHERE salary > (
                   SELECT AVG(salary) FROM employees e2 WHERE e2.department_id = e1.department_id
               )''',
            label="3. Employees earning more than department average:")

        # 4. EXISTS subquery: Employees in departments with at least one manager
        # What: Find employees in departments that have a manager.
        # Why: Filter for managed teams.
        # How: EXISTS subquery
        print_query(cursor,
            '''SELECT * FROM employees e WHERE EXISTS (
                   SELECT 1 FROM employees m WHERE m.department_id = e.department_id AND m.job_id LIKE '%MAN%'
               )''',
            label="4. Employees in departments with a manager:")

        # 5. APPLY-like: Add department average salary as a column (using join)
        # What: Annotate each employee with their department's average salary.
        # Why: For comparison and analytics.
        # How: Join with derived table
        print_query(cursor,
            '''SELECT e.*, d.avg_salary AS dept_avg_salary
               FROM employees e
               JOIN (SELECT department_id, AVG(salary) AS avg_salary FROM employees GROUP BY department_id) d
                 ON e.department_id = d.department_id
               LIMIT 10''',
            label="5. Employees with department average salary column:")
