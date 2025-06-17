from db_config import get_connection

try:
    conn = get_connection()
    print("✅ Connected to MySQL!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
