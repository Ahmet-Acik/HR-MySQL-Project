
# HR-MySQL-Project: Comprehensive MySQL & Python Practice

This project is a hands-on environment for learning and practicing MySQL database operations and data analysis with Python. It covers everything from basic SQL queries to advanced data manipulation, error handling, and visualization using best practices.

## Project Structure

- **scripts/**: Core scripts for database setup, config, data loading, and visualization.
- **mysql_practice/**: Modular Python scripts for practicing specific SQL and T-SQL topics with MySQL.
- **pandas_practice/**: Python scripts for practicing the same topics using pandas (and matplotlib where relevant). Each script mirrors the logic and learning objectives of its MySQL counterpart for side-by-side learning.
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


## Practice Modules

For each topic, there are two parallel sets of scripts:

- **MySQL Practice (`mysql_practice/`)**: Standalone Python scripts for each SQL/MySQL topic, using MySQL as the backend.
- **pandas Practice (`pandas_practice/`)**: Standalone Python scripts for each topic, using pandas DataFrames (and matplotlib where relevant) to demonstrate equivalent logic and analysis in Python.

### Topics Covered

| Topic # | MySQL Script | pandas Script |
| ------- | ------------------------------- | ----------------------------------- |
| 01 | 01_intro_to_tsql.py | 01_intro_to_pandas.py |
| 02 | 02_select_queries.py | 02_select_queries_pandas.py |
| 03 | 03_joins.py | 03_joins_pandas.py |
| 04 | 04_set_operators.py | 04_set_operators_pandas.py |
| 05 | 05_functions_aggregates.py | 05_functions_aggregates_pandas.py |
| 06 | 06_subqueries_apply.py | 06_subqueries_apply_pandas.py |
| 07 | 07_table_expressions.py | 07_table_expressions_pandas.py |
| 08 | 08_grouping_pivot.py | 08_grouping_pivot_pandas.py |
| 09 | 09_modifying_data.py | 09_modifying_data_pandas.py |
| 10 | 10_tsql_programming.py | 10_programming_pandas.py |
| 11 | 11_error_handling_transactions.py | 11_error_handling_transactions_pandas.py |

Run any module with:

```sh
python mysql_practice/<module_name>.py
python pandas_practice/<module_name>.py
```


## Best Practices

- Use environment variables for all credentials (`.env` + `python-dotenv`)
- Modularize code for clarity and reuse
- Use context managers (`with` statements) for DB connections and file operations
- Handle errors and transactions explicitly (both in SQL and pandas)
- All scripts include comprehensive examples, advanced patterns, and clear comments explaining what, why, and how

## Contributing

Pull requests and suggestions are welcome! Please open an issue for major changes.

## References

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)

## License

MIT
