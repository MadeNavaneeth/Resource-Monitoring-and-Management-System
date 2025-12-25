from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

def get_or_create_global_settings(db: Session) -> models.AlertSettings:
    """Helper to get GLOBAL settings (system_id=None), creating defaults if missing."""
    settings = db.query(models.AlertSettings).filter(models.AlertSettings.system_id == None).first()
    if not settings:
        settings = models.AlertSettings(
            system_id=None,
            cpu_threshold=90.0,
            memory_threshold=90.0,
            disk_threshold=90.0
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

def get_effective_settings(system_id: int, db: Session) -> models.AlertSettings:
    """Gets system-specific settings, falls back to global."""
    # 1. Try Specific
    specific = db.query(models.AlertSettings).filter(models.AlertSettings.system_id == system_id).first()
    if specific:
        return specific
    
    # 2. Fallback to Global
    return get_or_create_global_settings(db)

def check_thresholds(metric: schemas.MetricCreate, db: Session):
    """Evaluates metrics against thresholds and creates alerts if necessary."""
    
    settings = get_effective_settings(metric.system_id, db)
    alerts_to_create = []

    # Check CPU
    if metric.cpu_usage > settings.cpu_threshold:
        alerts_to_create.append({
            "type": "CPU",
            "message": f"High CPU usage detected: {metric.cpu_usage}% (Threshold: {settings.cpu_threshold}%)",
            "severity": "Critical" if metric.cpu_usage >= 95 else "Warning"
        })

    # Check Memory
    memory_percent = (metric.memory_used / metric.memory_total) * 100
    if memory_percent > settings.memory_threshold:
        alerts_to_create.append({
            "type": "Memory",
            "message": f"High Memory usage detected: {memory_percent:.2f}% (Threshold: {settings.memory_threshold}%)",
            "severity": "Critical" if memory_percent >= 95 else "Warning"
        })

    # Check Disk
    if metric.disk_usage > settings.disk_threshold:
        alerts_to_create.append({
            "type": "Disk",
            "message": f"High Disk usage detected: {metric.disk_usage}% (Threshold: {settings.disk_threshold}%)",
            "severity": "Critical"
        })

    if not alerts_to_create:
        return

    # Check for existing unresolved alerts to avoid spam
    # Optimization: Fetch all active alerts for system in one go
    active_alerts = db.query(models.Alert).filter(
        models.Alert.system_id == metric.system_id,
        models.Alert.is_resolved == False
    ).all()
    
    active_types = {a.alert_type for a in active_alerts}

    for alert_data in alerts_to_create:
        if alert_data["type"] not in active_types:
            new_alert = models.Alert(
                system_id=metric.system_id,
                alert_type=alert_data["type"],
                severity=alert_data["severity"],
                message=alert_data["message"]
            )
            db.add(new_alert)
    
    db.commit()
