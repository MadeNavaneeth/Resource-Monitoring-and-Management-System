
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('backend/resource_monitor.db')

# Query users
try:
    df = pd.read_sql_query("SELECT id, email, hashed_password, is_active FROM users", conn)
    print("\n--- USERS TABLE CONTENTS ---\n")
    print(df.to_string(index=False))
    print("\n----------------------------\n")
except Exception as e:
    print(e)
finally:
    conn.close()
