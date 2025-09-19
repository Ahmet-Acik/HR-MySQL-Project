"""
Querying Multiple Tables with JOIN
Comprehensive best-practice examples: INNER, LEFT, RIGHT, FULL OUTER (simulated), CROSS, SELF, multi-table joins
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


# INNER JOIN: Employees and their departments
def inner_join_employees_departments(cursor):
    cursor.execute('''
        SELECT e.first_name, e.last_name, d.department_name
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.department_id
        LIMIT 5;
    ''')
    return cursor.fetchall()

# LEFT JOIN: All employees, with department names (NULL if no department)
def left_join_employees_departments(cursor):
    cursor.execute('''
        SELECT e.first_name, e.last_name, d.department_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        LIMIT 5;
    ''')
    return cursor.fetchall()

# RIGHT JOIN: All departments, with employee names (NULL if no employee)
def right_join_departments_employees(cursor):
    cursor.execute('''
        SELECT d.department_name, e.first_name, e.last_name
        FROM departments d
        RIGHT JOIN employees e ON e.department_id = d.department_id
        LIMIT 5;
    ''')
    return cursor.fetchall()

# FULL OUTER JOIN (simulated with UNION)
def full_outer_join_employees_departments(cursor):
    cursor.execute('''
        SELECT e.first_name, e.last_name, d.department_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        UNION
        SELECT e.first_name, e.last_name, d.department_name
        FROM departments d
        LEFT JOIN employees e ON e.department_id = d.department_id
        LIMIT 5;
    ''')
    return cursor.fetchall()

# CROSS JOIN: All combinations of employees and departments (limit for demo)
def cross_join_employees_departments(cursor):
    cursor.execute('''
        SELECT e.first_name, d.department_name
        FROM employees e
        CROSS JOIN departments d
        LIMIT 5;
    ''')
    return cursor.fetchall()

# SELF JOIN: Employees and their managers
def self_join_employees_managers(cursor):
    cursor.execute('''
        SELECT e.first_name AS employee, m.first_name AS manager
        FROM employees e
        LEFT JOIN employees m ON e.manager_id = m.employee_id
        LIMIT 5;
    ''')
    return cursor.fetchall()

# Multi-table join: Employees, departments, and locations
def multi_table_join(cursor):
    cursor.execute('''
        SELECT e.first_name, d.department_name, l.city
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        JOIN locations l ON d.location_id = l.location_id
        LIMIT 5;
    ''')
    return cursor.fetchall()

def print_join_examples():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        print("INNER JOIN (employees & departments):")
        for row in inner_join_employees_departments(cursor):
            print(row)
        print("\nLEFT JOIN (all employees, departments):")
        for row in left_join_employees_departments(cursor):
            print(row)
        print("\nRIGHT JOIN (all departments, employees):")
        for row in right_join_departments_employees(cursor):
            print(row)
        print("\nFULL OUTER JOIN (simulated):")
        for row in full_outer_join_employees_departments(cursor):
            print(row)
        print("\nCROSS JOIN (employees x departments):")
        for row in cross_join_employees_departments(cursor):
            print(row)
        print("\nSELF JOIN (employees & managers):")
        for row in self_join_employees_managers(cursor):
            print(row)
        print("\nMULTI-TABLE JOIN (employees, departments, locations):")
        for row in multi_table_join(cursor):
            print(row)

if __name__ == "__main__":
    print_join_examples()
