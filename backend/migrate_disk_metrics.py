import sqlite3

def migrate():
    try:
        conn = sqlite3.connect('resource_monitor.db')
        cursor = conn.cursor()
        
        # Add columns
        print("Adding 'disk_read_bytes' column...")
        cursor.execute("ALTER TABLE metrics ADD COLUMN disk_read_bytes BIGINT DEFAULT 0")
        
        print("Adding 'disk_write_bytes' column...")
        cursor.execute("ALTER TABLE metrics ADD COLUMN disk_write_bytes BIGINT DEFAULT 0")
        
        conn.commit()
        print("✅ Migration successful: Disk I/O columns added.")
        conn.close()
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()
