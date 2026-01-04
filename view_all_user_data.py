"""
Complete script to view all user data from the database
"""
import sqlite3
import json
from datetime import datetime

def view_all_users():
    # Connect to database
    db_path = 'backend/resource_monitor.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("DATABASE LOCATION:")
    print(f"  {db_path}")
    print("=" * 80)
    
    # Get all users with full details
    cursor.execute("""
        SELECT id, email, hashed_password, is_active, created_at 
        FROM users 
        ORDER BY id
    """)
    
    users = cursor.fetchall()
    
    print(f"\n📊 TOTAL USERS: {len(users)}\n")
    
    for user in users:
        user_id, email, hashed_pw, is_active, created_at = user
        
        print("─" * 80)
        print(f"USER ID:       {user_id}")
        print(f"EMAIL:         {email}")
        print(f"PASSWORD HASH: {hashed_pw[:50]}... (truncated)")
        print(f"STATUS:        {'✅ Active' if is_active else '❌ Inactive'}")
        print(f"CREATED AT:    {created_at if created_at else 'N/A'}")
        print("─" * 80)
        print()
    
    # Show table structure
    print("\n📋 TABLE STRUCTURE:")
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    
    for col in columns:
        col_id, name, type_, not_null, default, pk = col
        print(f"  • {name:20} | Type: {type_:15} | Primary Key: {bool(pk)} | Not Null: {bool(not_null)}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("💡 HOW TO ACCESS THIS DATA:")
    print("=" * 80)
    print("1. Via Python:      python view_all_user_data.py")
    print("2. Via DB Browser:  Open 'backend/resource_monitor.db' in DB Browser for SQLite")
    print("3. Via API:         GET http://localhost:8000/api/users (if server is running)")
    print("4. Direct SQL:      sqlite3 backend/resource_monitor.db 'SELECT * FROM users;'")
    print("=" * 80)

if __name__ == "__main__":
    view_all_users()
