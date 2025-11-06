# db_config.py
import mysql.connector
from mysql.connector import Error
import socket

def get_db_connection():
    """Establishes a connection to the database with timeout."""
    try:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout for port check
            result = sock.connect_ex(('localhost', 3306))
            sock.close()
            
            if result != 0:
                # Port not accessible - MySQL not running
                return None
        except:
            # Socket check failed - assume MySQL not available
            return None
        
        # Try to connect - will timeout quickly if MySQL is not responding
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # <-- IMPORTANT: Change to your MySQL username
            password='Harsh2005@',  # <-- IMPORTANT: Change to your MySQL password
            database='DBMS_CP',
            autocommit=False,
            raise_on_warnings=False
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None
    except socket.timeout:
        print("Database connection timeout")
        return None
    except Exception as e:
        print(f"Unexpected error connecting to database: {e}")
        return None