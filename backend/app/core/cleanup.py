import time
import threading
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import models

logger = logging.getLogger(__name__)

CLEANUP_INTERVAL = 3600  # Run every hour
RETENTION_HOURS = 24     # Keep data for 24 hours

class MetricCleaner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()
        self.daemon = True

    def run(self):
        logger.info("Starting Metric Cleanup Task...")
        
        while not self.stop_event.is_set():
            try:
                self.cleanup_old_data()
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
            
            # Wait for interval or stop event
            self.stop_event.wait(CLEANUP_INTERVAL)

    def cleanup_old_data(self):
        db: Session = SessionLocal()
        try:
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=RETENTION_HOURS)
            
            # Delete old metrics
            deleted_count = db.query(models.Metric).filter(models.Metric.timestamp < cutoff_time).delete()
            db.commit()
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old metric records.")
                
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            db.rollback()
        finally:
            db.close()

    def stop(self):
        self.stop_event.set()
