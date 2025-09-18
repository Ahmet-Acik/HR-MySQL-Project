import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

HOST = os.environ.get('MYSQL_HOST', 'localhost')
USER = os.environ.get('MYSQL_USER')
PASSWORD = os.environ.get('MYSQL_PASSWORD')
DATABASE = os.environ.get('MYSQL_DATABASE', 'hr_db')

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), '..', 'hr_schema.sql')
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'hr_data.sql')


def execute_sql_file(cursor, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except Error as e:
                    print(f"\n[SQL ERROR]\nCommand: {command}\nError: {e}\n")


def main():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        cursor = connection.cursor()
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        cursor.execute(f"USE {DATABASE}")
        print(f"Using database: {DATABASE}")

        # Drop all tables in correct order to avoid FK issues
        drop_order = [
            'dependents',
            'employees',
            'departments',
            'jobs',
            'locations',
            'countries',
            'regions'
        ]
        for table in drop_order:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            except Error as e:
                print(f"Error dropping table {table}: {e}")

        print("Executing schema file...")
        execute_sql_file(cursor, SCHEMA_FILE)
        print("Schema created.")

        print("Executing data file...")
        execute_sql_file(cursor, DATA_FILE)
        connection.commit()
        print("Data loaded.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
