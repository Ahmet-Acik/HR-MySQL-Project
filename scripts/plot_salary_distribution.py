import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from db_config import HOST, USER, PASSWORD, DATABASE

conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

# Load salary data
df = pd.read_sql('SELECT salary FROM employees', conn)

plt.hist(df['salary'], bins=20, color='skyblue', edgecolor='black')
plt.title('Salary Distribution')
plt.xlabel('Salary')
plt.ylabel('Frequency')
plt.show()

conn.close()
