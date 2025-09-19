"""
Using Set Operators (UNION, INTERSECT, EXCEPT)
Best practices: UNION, UNION ALL, INTERSECT (simulated), EXCEPT (simulated)
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


# UNION: Unique values from both queries
def union_employees_departments(cursor):
    cursor.execute('''
        SELECT first_name AS name FROM employees
        UNION
        SELECT department_name AS name FROM departments;
    ''')
    return cursor.fetchall()

# UNION ALL: All values from both queries (including duplicates)
def union_all_employees_departments(cursor):
    cursor.execute('''
        SELECT first_name AS name FROM employees
        UNION ALL
        SELECT department_name AS name FROM departments;
    ''')
    return cursor.fetchall()

# INTERSECT simulation: Values present in both tables
def intersect_employees_departments(cursor):
    cursor.execute('''
        SELECT first_name AS name FROM employees
        WHERE first_name IN (SELECT department_name FROM departments);
    ''')
    return cursor.fetchall()

# EXCEPT simulation: Values in employees not in departments
def except_employees_departments(cursor):
    cursor.execute('''
        SELECT first_name AS name FROM employees
        WHERE first_name NOT IN (SELECT department_name FROM departments);
    ''')
    return cursor.fetchall()

def print_set_operator_examples():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        print("UNION (unique names from employees and departments):")
        for row in union_employees_departments(cursor):
            print(row)
        print("\nUNION ALL (all names, including duplicates):")
        for row in union_all_employees_departments(cursor):
            print(row)
        print("\nINTERSECT (names present in both employees and departments):")
        for row in intersect_employees_departments(cursor):
            print(row)
        print("\nEXCEPT (names in employees not in departments):")
        for row in except_employees_departments(cursor):
            print(row)

if __name__ == "__main__":
    print_set_operator_examples()
