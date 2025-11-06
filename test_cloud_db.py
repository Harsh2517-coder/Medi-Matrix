from db_config import get_db_connection

conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("📋 Tables in your Clever Cloud database:")
    for t in tables:
        print("-", t[0])
    cursor.close()
    conn.close()
else:
    print("❌ Connection failed.")
