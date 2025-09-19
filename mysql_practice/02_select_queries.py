"""
Querying Tables with SELECT
Best practices: all examples in functions, modular, only SELECT statements, clear output
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

def select_all_employees(cursor):
    cursor.execute("SELECT * FROM employees;")
    return cursor.fetchall()

def select_employees_by_department(cursor, department_id):
    cursor.execute("SELECT * FROM employees WHERE department_id = %s;", (department_id,))
    return cursor.fetchall()

def select_employee_by_id(cursor, employee_id):
    cursor.execute("SELECT * FROM employees WHERE employee_id = %s;", (employee_id,))
    return cursor.fetchone()

def select_employees_by_job_title(cursor, job_title):
    query = (
        "SELECT e.* FROM employees e "
        "JOIN jobs j ON e.job_id = j.job_id "
        "WHERE j.job_title LIKE %s;"
    )
    cursor.execute(query, (f"%{job_title}%",))
    return cursor.fetchall()

def select_first_n_employees(cursor, n=5):
    cursor.execute("SELECT * FROM employees LIMIT %s;", (n,))
    return cursor.fetchall()

def select_employees_with_salary_above(cursor, amount):
    cursor.execute("SELECT * FROM employees WHERE salary > %s;", (amount,))
    return cursor.fetchall()

def print_example_results():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        print("All employees:")
        for row in select_all_employees(cursor):
            print(row)
        print("\nEmployees in department 1:")
        for row in select_employees_by_department(cursor, 1):
            print(row)
        print("\nEmployee with ID 101:")
        print(select_employee_by_id(cursor, 101))
        print("\nEmployees with job title 'Manager':")
        for row in select_employees_by_job_title(cursor, 'Manager'):
            print(row)
        print("\nFirst 5 employees:")
        for row in select_first_n_employees(cursor, 5):
            print(row)
        print("\nEmployees with salary > 5000:")
        for row in select_employees_with_salary_above(cursor, 5000):
            print(row)

if __name__ == "__main__":
    print_example_results()