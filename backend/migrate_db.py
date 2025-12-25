import sqlite3

def migrate():
    conn = None # Initialize conn to None
    try:
        conn = sqlite3.connect('resource_monitor.db')
        cursor = conn.cursor()
        
        # 1. Add 'drivers' to 'systems' table
        print("Checking for 'drivers' column in 'systems'...")
        cursor.execute("PRAGMA table_info(systems)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'drivers' not in columns:
            print("Adding 'drivers' column...")
            cursor.execute("ALTER TABLE systems ADD COLUMN drivers JSON")
            conn.commit()
            print("Added 'drivers' column.")
        else:
            print("'drivers' column already exists.")

        # 2. Add 'memory_used' to 'metrics' table
        print("Checking for 'memory_used' column in 'metrics'...")
        cursor.execute("PRAGMA table_info(metrics)")
        metric_columns = [info[1] for info in cursor.fetchall()]
        if 'memory_used' not in metric_columns:
            print("Adding 'memory_used' column...")
            cursor.execute("ALTER TABLE metrics ADD COLUMN memory_used BIGINT")
            conn.commit()
            print("Added 'memory_used' column.")
        else:
            print("'memory_used' column already exists.")

        # 3. Add 'disk_free' to 'metrics' table (Missed earlier?)
        if 'disk_free' not in metric_columns:
            print("Adding 'disk_free' column...")
            cursor.execute("ALTER TABLE metrics ADD COLUMN disk_free BIGINT")
            conn.commit()
            print("Added 'disk_free' column.")
        else:
            print("'disk_free' column already exists.")

        print("✅ Migration checks complete.")

    except sqlite3.OperationalError as e:
        print(f"Error during migration: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate()
