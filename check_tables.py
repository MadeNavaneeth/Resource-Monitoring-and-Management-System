import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('backend/resource_monitor.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\n=== ALL TABLES IN DATABASE ===")
for table in tables:
    print(f"  - {table[0]}")

# Check if s_admins exists
print("\n=== CHECKING FOR s_admins TABLE ===")
try:
    df = pd.read_sql_query("SELECT * FROM s_admins", conn)
    print("\n--- s_admins TABLE CONTENTS ---")
    print(df.to_string(index=False))
    print("\n--- COLUMN INFO ---")
    cursor.execute("PRAGMA table_info(s_admins)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  Column: {col[1]} | Type: {col[2]} | Nullable: {not col[3]}")
except Exception as e:
    print(f"Error: {e}")

conn.close()
