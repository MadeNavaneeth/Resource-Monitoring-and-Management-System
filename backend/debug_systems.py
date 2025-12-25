from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./resource_monitor.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_systems():
    db = SessionLocal()
    try:
        # Check systems count
        result = db.execute(text("SELECT id, hostname, last_seen, is_active FROM systems"))
        systems = result.fetchall()
        print(f"Total Systems Found: {len(systems)}")
        for sys in systems:
            print(f" - ID: {sys.id} | Host: {sys.hostname} | Active: {sys.is_active} | Seen: {sys.last_seen}")
    except Exception as e:
        with open("db_error.log", "w") as f:
            f.write(str(e))
        print(f"Error checking DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_systems()
