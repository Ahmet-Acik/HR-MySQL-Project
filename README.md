# HR Data Analysis with MySQL, Pandas, and Matplotlib

This project demonstrates how to use Python with MySQL, pandas, and matplotlib to analyze HR data. It includes sample scripts for connecting to a MySQL database, loading data into pandas, and visualizing results.

## Requirements

- Python 3.8+
- MySQL server (local or remote)
- The following Python packages (see requirements.txt)

## Setup

1. Install Python dependencies:

   ```sh
   pip install -r requirements.txt
   ```

2. Set up your MySQL server and import the HR schema/data (see `mysql_hr_schema.sql` and `mysql_hr_data.sql`).
3. Update the database connection settings in `scripts/db_config.py`.

## Example Scripts

- `scripts/mysql_connect.py`: Test MySQL connection
- `scripts/load_hr_data.py`: Load HR data into pandas DataFrames
- `scripts/plot_salary_distribution.py`: Visualize salary data

## License

MIT
