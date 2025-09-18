
# MySQL database configuration using environment variables
import os
from dotenv import load_dotenv

# Automatically load environment variables from a .env file
load_dotenv()

HOST = os.environ.get('MYSQL_HOST', 'localhost')
USER = os.environ.get('MYSQL_USER')
PASSWORD = os.environ.get('MYSQL_PASSWORD')
DATABASE = os.environ.get('MYSQL_DATABASE', 'hr_db')
