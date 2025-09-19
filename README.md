
# HR-MySQL-Project: Comprehensive MySQL & Python Practice

This project is a hands-on environment for learning and practicing MySQL database operations and data analysis with Python. It covers everything from basic SQL queries to advanced data manipulation, error handling, and visualization using best practices.

## Project Structure

- **scripts/**: Core scripts for database setup, config, data loading, and visualization.
- **mysql_practice/**: Modular Python scripts for practicing specific SQL and T-SQL topics with MySQL.
- **hr_schema.sql / hr_data.sql**: MySQL-compatible schema and sample HR data.
- **.env**: Environment variables for secure database credentials (never commit secrets!).

## Learning Goals

- Master MySQL basics and advanced features using Python
- Practice real-world SQL scenarios: SELECT, JOIN, aggregation, subqueries, DML, error handling, and more
- Learn best practices for Python-MySQL integration (env vars, modular code, error handling)

## Requirements

- Python 3.8+
- MySQL server (local or remote)
- See `requirements.txt` for Python dependencies

## Setup

1. Install Python dependencies:

   ```sh
   pip install -r requirements.txt
   ```

2. Set up your MySQL server and import the schema/data:

   ```sh
   mysql -u <user> -p < hr_schema.sql
   mysql -u <user> -p < hr_data.sql
   ```

3. Copy `.env` and set your MySQL credentials:

   ```env
   MYSQL_HOST=localhost
   MYSQL_USER=your_user
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=hr_db
   ```

4. All scripts use `scripts/db_config.py` for secure credential loading.

## Example Scripts

- `scripts/mysql_connect.py`: Test MySQL connection
- `scripts/load_hr_data.py`: Load HR data into pandas DataFrames
- `scripts/plot_salary_distribution.py`: Visualize salary data
- `scripts/setup_database.py`: Automate schema/data loading

## Practice Modules (`mysql_practice/`)

Each file is a standalone Python script for a key SQL/MySQL topic:

- `01_intro_to_tsql.py`: Introduction to Transact-SQL and MySQL with Python
- `02_select_queries.py`: Querying tables with SELECT
- `03_joins.py`: Querying multiple tables with JOIN
- `04_set_operators.py`: Using set operators (UNION, etc.)
- `05_functions_aggregates.py`: Using functions and aggregating data
- `06_subqueries_apply.py`: Using subqueries
- `07_table_expressions.py`: Using table expressions (CTE, derived tables)
- `08_grouping_pivot.py`: Grouping sets and pivoting data
- `09_modifying_data.py`: Modifying data (INSERT, UPDATE, DELETE)
- `10_tsql_programming.py`: Programming with T-SQL (MySQL style)
- `11_error_handling_transactions.py`: Error handling and transactions

Run any module with:

```sh
python mysql_practice/<module_name>.py
```

## Best Practices

- Use environment variables for all credentials (`.env` + `python-dotenv`)
- Modularize code for clarity and reuse
- Use context managers (`with` statements) for DB connections
- Handle errors and transactions explicitly

## Contributing

Pull requests and suggestions are welcome! Please open an issue for major changes.

## References

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)

## License

MIT
