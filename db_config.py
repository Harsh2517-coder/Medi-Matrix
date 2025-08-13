# db_config.py
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # <-- IMPORTANT: Change to your MySQL username
            password='Harsh2005@',  # <-- IMPORTANT: Change to your MySQL password
            database='DBMS_CP'
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None