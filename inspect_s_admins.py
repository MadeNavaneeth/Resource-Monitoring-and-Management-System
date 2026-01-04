import sqlite3
import sys

# Connect to database
conn = sqlite3.connect('backend/resource_monitor.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print("\n=== ALL TABLES IN DATABASE ===")
for table in tables:
    print(f"  - {table}")

# Check if s_admins exists
if "s_admins" in tables:
    print("\n✅ s_admins table FOUND!")
    
    # Get table info
    print("\n=== TABLE STRUCTURE ===")
    cursor.execute("PRAGMA table_info(s_admins)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]:20} | Type: {col[2]:10} | Primary Key: {bool(col[5])} | Not Null: {bool(col[3])}")
    
    # Get data
    print("\n=== TABLE DATA ===")
    cursor.execute("SELECT * FROM s_admins")
    rows = cursor.fetchall()
    
    # Print header
    col_names = [col[1] for col in columns]
    print(" | ".join(col_names))
    print("-" * 80)
    
    # Print rows
    for row in rows:
        print(" | ".join(str(item)[:30] if item else "NULL" for item in row))
    
    print(f"\nTotal rows: {len(rows)}")
else:
    print("\n❌ s_admins table NOT FOUND!")

conn.close()
