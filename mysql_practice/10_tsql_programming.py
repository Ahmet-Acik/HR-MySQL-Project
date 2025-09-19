"""
Programming with Transact-SQL (T-SQL) in MySQL
- Variables, control flow, stored procedures (MySQL style), parameterized procedures, error handling

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


def print_result(label, result):
    print(f"\n{label}")
    if isinstance(result, list):
        for row in result:
            print(row)
    else:
        print(result)

if __name__ == "__main__":
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # 1. Variables and control flow
            # What: Use variables and IF/ELSE logic in SQL
            # Why: Demonstrate procedural logic
            print("\n1. Variables and control flow:")
            cursor.execute("SET @dept_id = 10;")
            cursor.execute("SELECT IF(@dept_id = 10, 'Ten', 'Other') AS dept_label;")
            print(cursor.fetchall())

            # 2. Stored procedure: count employees
            # What: Encapsulate logic for reuse
            # Why: Modularize business logic
            cursor.execute("DROP PROCEDURE IF EXISTS get_employee_count;")
            cursor.execute("""
                CREATE PROCEDURE get_employee_count()
                BEGIN
                    SELECT COUNT(*) AS employee_count FROM employees;
                END;
            """)
            cursor.callproc('get_employee_count')
            for result in cursor.stored_results():
                print_result("2. Employee count (stored procedure):", result.fetchall())

            # 3. Parameterized stored procedure: employees in department
            # What: Return employees in a given department
            # Why: Encapsulate logic with parameters
            cursor.execute("DROP PROCEDURE IF EXISTS employees_in_department;")
            cursor.execute("""
                CREATE PROCEDURE employees_in_department(IN dept_id INT)
                BEGIN
                    SELECT * FROM employees WHERE department_id = dept_id;
                END;
            """)
            cursor.callproc('employees_in_department', [10])
            for result in cursor.stored_results():
                print_result("3. Employees in department 10 (parameterized procedure):", result.fetchall())

            # 4. Error handling (simple)
            # What: Demonstrate error handling in stored procedure
            # Why: Robustness
            cursor.execute("DROP PROCEDURE IF EXISTS safe_divide;")
            cursor.execute("""
                CREATE PROCEDURE safe_divide(IN a INT, IN b INT, OUT result DECIMAL(10,2))
                BEGIN
                    IF b = 0 THEN
                        SET result = NULL;
                    ELSE
                        SET result = a / b;
                    END IF;
                END;
            """)
            # Call safe_divide with b=0
            args = [10, 0, 0]
            result_args = cursor.callproc('safe_divide', args)
            print_result("4. Error handling (safe divide, b=0):", result_args)

    except Exception as e:
        print("Error during T-SQL programming examples:", e)
