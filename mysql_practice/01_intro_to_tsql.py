"""
Introduction to Transact-SQL (T-SQL) with MySQL and Python
- How to connect to MySQL
- Basic query examples
"""
from scripts.db_config import HOST, USER, PASSWORD, DATABASE
import mysql.connector

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

if __name__ == "__main__":
    with get_connection() as conn:
        print("Connected to MySQL!")
