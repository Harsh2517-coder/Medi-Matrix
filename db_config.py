# db_config.py
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Establishes a connection to the Clever Cloud MySQL database."""
    try:
        conn = mysql.connector.connect(
            host='birtodrqxg8z06h3jzyn-mysql.services.clever-cloud.com',  # <-- Host
            user='uh9w7xnudzctr4cx',                                     # <-- User
            password='eN19C2F9YExBrY6VgY6I',                             # <-- Password
            database='birtodrqxg8z06h3jzyn',                             # <-- Database Name
            port=3306,                                                   # <-- Port
            autocommit=False,
            raise_on_warnings=False
        )

        if conn.is_connected():
            print("✅ Successfully connected to Clever Cloud MySQL database!")
        return conn

    except Error as e:
        print(f"❌ Error connecting to MySQL Database: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error connecting to database: {e}")
        return None
