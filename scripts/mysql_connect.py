import mysql.connector
from db_config import HOST, USER, PASSWORD, DATABASE

try:
    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    print("MySQL connection successful!")
    conn.close()
except Exception as e:
    print(f"MySQL connection failed: {e}")
