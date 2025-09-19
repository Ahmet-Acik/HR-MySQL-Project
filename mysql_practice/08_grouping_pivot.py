"""
Grouping Sets and Pivoting Data
- MySQL supports GROUPING SETS (from 8.0.18+), ROLLUP, and CUBE, but not PIVOT directly
- Pivoting can be simulated with conditional aggregation

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

        # 1. Basic group by: count employees by department and job
        # What: Count employees for each department/job combination.
        # Why: See job distribution per department.
        print_query(cursor,
            '''SELECT department_id, job_id, COUNT(*) as num_employees
               FROM employees
               GROUP BY department_id, job_id''',
            label="1. Count employees by department and job:")

        # 2. ROLLUP: add subtotals by department and grand total
        # What: Add department totals and overall total.
        # Why: Summarize at multiple levels.
        print_query(cursor,
            '''SELECT department_id, job_id, COUNT(*) as num_employees
               FROM employees
               GROUP BY department_id, job_id WITH ROLLUP''',
            label="2. ROLLUP (subtotals and grand total):")

        # 3. GROUPING SETS: custom subtotal/grouping combinations (if supported)
        # What: Custom subtotal/grouping combinations.
        # Why: Flexible summary tables.
        try:
            print_query(cursor,
                '''SELECT department_id, job_id, COUNT(*) as num_employees
                   FROM employees
                   GROUP BY GROUPING SETS ((department_id, job_id), (department_id), ())''',
                label="3. GROUPING SETS (if supported):")
        except Exception as e:
            print("GROUPING SETS not supported on this MySQL version:", e)

        # 4. Pivot simulation: departments as rows, jobs as columns
        # What: Pivot to see job counts per department in a matrix.
        # Why: Easier comparison across jobs/departments.
        # How: Conditional aggregation
        print_query(cursor,
            '''SELECT department_id
                      , SUM(CASE WHEN job_id = 'IT_PROG' THEN 1 ELSE 0 END) AS IT_PROG
                      , SUM(CASE WHEN job_id = 'SA_REP' THEN 1 ELSE 0 END) AS SA_REP
                      , SUM(CASE WHEN job_id = 'FI_ACCOUNT' THEN 1 ELSE 0 END) AS FI_ACCOUNT
                      , SUM(CASE WHEN job_id = 'AD_VP' THEN 1 ELSE 0 END) AS AD_VP
                      , SUM(CASE WHEN job_id = 'AD_PRES' THEN 1 ELSE 0 END) AS AD_PRES
                      , SUM(CASE WHEN job_id = 'PU_CLERK' THEN 1 ELSE 0 END) AS PU_CLERK
                      , SUM(CASE WHEN job_id = 'ST_CLERK' THEN 1 ELSE 0 END) AS ST_CLERK
                      , SUM(CASE WHEN job_id = 'SH_CLERK' THEN 1 ELSE 0 END) AS SH_CLERK
                      , SUM(CASE WHEN job_id = 'MK_MAN' THEN 1 ELSE 0 END) AS MK_MAN
                      , SUM(CASE WHEN job_id = 'MK_REP' THEN 1 ELSE 0 END) AS MK_REP
               FROM employees
               GROUP BY department_id''',
            label="4. Pivot simulation (departments as rows, jobs as columns):")

        # 5. Unpivot simulation: convert wide to long format (using UNION ALL)
        # What: Unpivot the previous pivot table.
        # Why: Prepare for further analysis or visualization.
        print_query(cursor,
            '''SELECT department_id, 'IT_PROG' AS job_id, SUM(CASE WHEN job_id = 'IT_PROG' THEN 1 ELSE 0 END) AS num_employees FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'SA_REP', SUM(CASE WHEN job_id = 'SA_REP' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'FI_ACCOUNT', SUM(CASE WHEN job_id = 'FI_ACCOUNT' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'AD_VP', SUM(CASE WHEN job_id = 'AD_VP' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'AD_PRES', SUM(CASE WHEN job_id = 'AD_PRES' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'PU_CLERK', SUM(CASE WHEN job_id = 'PU_CLERK' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'ST_CLERK', SUM(CASE WHEN job_id = 'ST_CLERK' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'SH_CLERK', SUM(CASE WHEN job_id = 'SH_CLERK' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'MK_MAN', SUM(CASE WHEN job_id = 'MK_MAN' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id
               UNION ALL
               SELECT department_id, 'MK_REP', SUM(CASE WHEN job_id = 'MK_REP' THEN 1 ELSE 0 END) FROM employees GROUP BY department_id''',
            label="5. Unpivot simulation (wide to long):")
