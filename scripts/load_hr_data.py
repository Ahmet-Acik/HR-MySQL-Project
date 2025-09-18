import mysql.connector
import pandas as pd
from db_config import HOST, USER, PASSWORD, DATABASE

conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

# Example: Load employees table into pandas DataFrame
df = pd.read_sql('SELECT * FROM employees', conn)
print(df.head())

conn.close()
