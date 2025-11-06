from db_config import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SHOW TABLES;")
for table in cursor.fetchall():
    print(table)
cursor.close()
conn.close()
