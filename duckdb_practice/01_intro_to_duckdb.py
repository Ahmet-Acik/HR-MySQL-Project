"""
Introduction to DuckDB with Python
- How to connect, load data, and run a simple query
"""
import duckdb
import pandas as pd

def main():
    # Connect to DuckDB in-memory
    con = duckdb.connect()
    # Load CSV as table
    con.execute("CREATE TABLE employees AS SELECT * FROM read_csv_auto('../data/employees.csv')")
    # Simple SELECT
    result = con.execute("SELECT * FROM employees LIMIT 5").fetchdf()
    print(result)
    con.close()

if __name__ == "__main__":
    main()
