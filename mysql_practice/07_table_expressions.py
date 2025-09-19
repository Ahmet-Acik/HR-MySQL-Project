"""
Using Table Expressions (CTE, Derived Tables)
- MySQL supports CTEs (WITH ...), derived tables, nested CTEs, multi-step CTEs, and inline views

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

        # 1. Derived table: Employees with salary > 10000
        # What: Filter employees with high salary.
        # Why: Focus on high earners.
        # How: Use a subquery in FROM (derived table)
        print_query(cursor,
            '''SELECT * FROM (SELECT * FROM employees WHERE salary > 10000) AS high_salary''',
            label="1. Employees with salary > 10000 (derived table):")

        # 2. CTE: Employees with salary > 10000, then count by department
        # What: Employees with salary > 10000, then count by department
        # Why: See which departments have high earners.
        # How: Use CTE for reusability
        print_query(cursor,
            '''WITH high_salary AS (
                   SELECT * FROM employees WHERE salary > 10000
               )
               SELECT department_id, COUNT(*) AS num_high_earners FROM high_salary GROUP BY department_id''',
            label="2. High salary count by department (CTE):")

        # 3. Nested derived tables: Top 3 earners per department
        # What: For each department, get top 3 salaries.
        # Why: Identify top earners per team.
        # How: Use ROW_NUMBER() in a derived table
        print_query(cursor,
            '''SELECT * FROM (
                   SELECT *, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
                   FROM employees
               ) ranked WHERE rnk <= 3
               ORDER BY department_id, rnk''',
            label="3. Top 3 earners per department (nested derived table):")

        # 4. Multi-step CTE: Employees with salary > 5000, then those in departments with >5 such employees
        # What: Employees with salary > 5000, then those in large departments
        # Why: Find large, well-paid teams.
        print_query(cursor,
            '''WITH high_paid AS (
                   SELECT * FROM employees WHERE salary > 5000
               ),
               large_depts AS (
                   SELECT department_id FROM high_paid GROUP BY department_id HAVING COUNT(*) > 5
               )
               SELECT * FROM high_paid WHERE department_id IN (SELECT department_id FROM large_depts)''',
            label="4. Employees with salary > 5000 in large departments (multi-step CTE):")

        # 5. Inline view: Join high_salary with departments info
        # What: Join high_salary with departments info
        # Why: Add department names to high earners
        print_query(cursor,
            '''WITH high_salary AS (
                   SELECT * FROM employees WHERE salary > 10000
               )
               SELECT h.*, d.department_name FROM high_salary h
               LEFT JOIN departments d ON h.department_id = d.department_id''',
            label="5. High salary employees with department info (inline view):")
