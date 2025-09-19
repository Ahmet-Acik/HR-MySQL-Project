"""
Error Handling and Transactions
- Using try/except in Python
- MySQL transaction control (COMMIT, ROLLBACK, SAVEPOINT)
- Best practices for robust data operations

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


def print_salaries(cursor, label=None):
    if label:
        print(f"\n{label}")
    cursor.execute("SELECT employee_id, salary FROM employees ORDER BY employee_id DESC LIMIT 5;")
    for row in cursor.fetchall():
        print(row)

if __name__ == "__main__":
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Basic transaction: commit/rollback
        # What: Try to update salaries, rollback on error.
        # Why: Ensure data integrity.
        cursor.execute("START TRANSACTION;")
        print_salaries(cursor, label="Original salaries (last 5):")
        try:
            cursor.execute("UPDATE employees SET salary = salary * 1.1 WHERE department_id = 10;")
            raise Exception("Simulated error: rolling back!")
            conn.commit()
        except Exception as e:
            print(f"\nError occurred: {e}. Rolling back.")
            conn.rollback()
        print_salaries(cursor, label="After simulated rollback (should match original):")

        # 2. Commit: Only apply changes if no error
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute("UPDATE employees SET salary = salary * 1.1 WHERE department_id = 10;")
            # No error, so commit
            conn.commit()
            print_salaries(cursor, label="After commit (salaries updated):")
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()

        # 3. Using SAVEPOINT for partial rollback
        # What: Rollback only part of a transaction.
        # Why: Fine-grained error recovery.
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute("UPDATE employees SET salary = salary * 1.05 WHERE department_id = 10;")
            cursor.execute("SAVEPOINT before_bonus;")
            cursor.execute("UPDATE employees SET salary = salary + 1000 WHERE department_id = 10;")
            raise Exception("Simulated error after bonus: partial rollback!")
        except Exception as e:
            print(f"\nError occurred: {e}. Rolling back to SAVEPOINT.")
            cursor.execute("ROLLBACK TO SAVEPOINT before_bonus;")
            conn.commit()
        print_salaries(cursor, label="After partial rollback (should reflect only 5% raise):")

        # 4. Error handling in data processing
        # What: Handle errors in SQL execution.
        # Why: Robust data pipelines.
        try:
            cursor.execute("SELECT salary, bonus FROM employees LIMIT 1;")
        except Exception as e:
            print(f"\nHandled data processing error: {e}")

    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if conn is not None:
            conn.close()
