import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('sysmonitor.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(systems)")
        columns = [info[1] for info in cursor.fetchall()]
        print(f"Columns in 'systems': {columns}")
        
        if 'drivers' in columns:
            print("✅ 'drivers' column EXISTS.")
        else:
            print("❌ 'drivers' column MISSING.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
