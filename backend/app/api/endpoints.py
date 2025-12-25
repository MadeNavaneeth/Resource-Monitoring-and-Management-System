from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone
import uuid
import csv
import io
from fastapi.responses import StreamingResponse

from app.db.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

from app.core.security import get_api_key, get_current_user
from app.core.alerts import check_thresholds

# --- System Endpoints ---

@router.post("/systems/register", response_model=schemas.System, dependencies=[Depends(get_api_key)])
def register_system(system: schemas.SystemCreate, db: Session = Depends(get_db)):
    db_system = db.query(models.System).filter(models.System.hostname == system.hostname).first()
    if db_system:
        # Update existing system with all new fields
        for field, value in system.dict().items():
            if value is not None:
                setattr(db_system, field, value)
        db_system.is_active = True
        db_system.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_system)
        return db_system
    
    new_system = models.System(**system.dict(), last_seen=datetime.now(timezone.utc))
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    return new_system

@router.get("/systems", response_model=List[schemas.System])
def get_systems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Mark stale systems as offline (60 seconds to allow for network delays)
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=60)
    db.query(models.System).filter(
        models.System.last_seen < cutoff,
        models.System.is_active == True
    ).update({"is_active": False})
    db.commit()

    systems = db.query(models.System).offset(skip).limit(limit).all()
    return systems

@router.get("/systems/{system_id}", response_model=schemas.System)
def get_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    # Check status on single fetch too
    if system.is_active and system.last_seen:
         # Ensure both are offset-aware for comparison
         last_seen = system.last_seen
         if last_seen.tzinfo is None:
             last_seen = last_seen.replace(tzinfo=timezone.utc)
             
         cutoff = datetime.now(timezone.utc) - timedelta(seconds=60)
         if last_seen < cutoff:
             system.is_active = False
             db.commit()
             db.refresh(system)

    return system

@router.delete("/systems/{system_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def delete_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    # Cascade deletes metrics and alerts automatically
    db.delete(system)
    db.commit()
    return None

# --- Metric Endpoints ---

@router.post("/metrics", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_api_key)])
def create_metric(
    metric: schemas.MetricCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    system = db.query(models.System).filter(models.System.id == metric.system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    # Update system heatlh
    system.last_seen = datetime.now(timezone.utc)
    system.is_active = True # If sending metrics, it is active
    
    # Save Metric to DB
    new_metric = models.Metric(
        system_id=metric.system_id,
        cpu_usage=metric.cpu_usage,
        memory_percent=metric.memory_percent,
        memory_used=metric.memory_used,
        disk_usage=metric.disk_usage,
        network_sent=metric.network_sent,
        network_recv=metric.network_recv,
        process_count=metric.process_count,
        boot_time=metric.boot_time,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)

    # Pruning: Delete metrics older than 24 hours for this system (simple cleanup)
    # To optimize, run this only occasionally or in background, but for now specific per-request is safe for low load.
    # actually let's do it with 1% probability or just every time if it's indexed? Index on timestamp helps.
    # Let's keep it simple: No auto-prune on every request (slow).
    # We will rely on user 'Restarting' to not matter, but disk space grows.
    # User wanted history.
    
    background_tasks.add_task(check_thresholds, metric, db)
    
    return {"id": new_metric.id, "status": "stored"}

@router.get("/metrics/{system_id}")
def get_metrics_history(system_id: int, limit: int = 100, db: Session = Depends(get_db)):
    # Fetch from DB
    metrics = db.query(models.Metric)\
        .filter(models.Metric.system_id == system_id)\
        .order_by(models.Metric.timestamp.desc())\
        .limit(limit)\
        .all()
    return metrics

@router.get("/metrics/{system_id}/export")
def export_metrics(system_id: int, db: Session = Depends(get_db)):
    metrics = db.query(models.Metric)\
        .filter(models.Metric.system_id == system_id)\
        .order_by(models.Metric.timestamp.desc())\
        .limit(10000)\
        .all()
        
    if not metrics:
        raise HTTPException(status_code=404, detail="No metrics found for this system")

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Timestamp", "CPU (%)", "Memory (%)", "Memory Used (MB)", 
        "Disk (%)", "Net Sent (Bytes)", "Net Recv (Bytes)", 
        "Process Count", "Boot Time"
    ])
    
    # Rows
    for m in metrics:
        writer.writerow([
            m.timestamp, m.cpu_usage, m.memory_percent, m.memory_used,
            m.disk_usage, m.network_sent, m.network_recv,
            m.process_count, m.boot_time
        ])
        
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=system_{system_id}_metrics.csv"}
    )

# --- Alert Endpoints ---

@router.get("/alerts", response_model=List[schemas.Alert])
def get_alerts(skip: int = 0, limit: int = 100, is_resolved: bool = False, db: Session = Depends(get_db)):
    alerts = db.query(models.Alert).filter(models.Alert.is_resolved == is_resolved).offset(skip).limit(limit).all()
    return alerts

@router.put("/alerts/{alert_id}/resolve", response_model=schemas.Alert)
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    db.commit()
    db.refresh(alert)
    return alert

# --- Alert Settings Endpoints ---

# from app.core.alerts import get_or_create_settings

@router.get("/alerts/settings", response_model=schemas.AlertSettings)
def get_alert_settings(system_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get alert settings. 
    If system_id is provided, returns specific settings (or 404/Global depending on preference? 
    Actually, usually we want to know if specific exist or not).
    
    Let's return the EFFECTIVE settings for a system if system_id is passed,
    or the Global settings if system_id is None.
    """
    from app.core.alerts import get_or_create_global_settings, get_effective_settings
    
    if system_id:
        return get_effective_settings(system_id, db)
    else:
        return get_or_create_global_settings(db)

@router.put("/alerts/settings", response_model=schemas.AlertSettings)
def update_alert_settings(settings: schemas.AlertSettingsCreate, db: Session = Depends(get_db)):
    """
    Update alert settings.
    If settings.system_id is Set, we update/create specific settings.
    If settings.system_id is None, we update Global settings.
    """
    from app.core.alerts import get_or_create_global_settings
    
    target_system_id = settings.system_id
    
    db_settings = None
    if target_system_id is None:
        # Updating Global
        db_settings = get_or_create_global_settings(db)
    else:
        # Updating Specific
        db_settings = db.query(models.AlertSettings).filter(models.AlertSettings.system_id == target_system_id).first()
        if not db_settings:
            db_settings = models.AlertSettings(system_id=target_system_id)
            db.add(db_settings)
            
    # Validate Inputs
    if not (0 <= settings.cpu_threshold <= 100):
        raise HTTPException(status_code=400, detail="CPU threshold must be 0-100")
    if not (0 <= settings.memory_threshold <= 100):
         raise HTTPException(status_code=400, detail="Memory threshold must be 0-100")
    if not (0 <= settings.disk_threshold <= 100):
         raise HTTPException(status_code=400, detail="Disk threshold must be 0-100")

    db_settings.cpu_threshold = settings.cpu_threshold
    db_settings.memory_threshold = settings.memory_threshold
    db_settings.disk_threshold = settings.disk_threshold
    
    db.commit()
    db.refresh(db_settings)
    return db_settings

# --- User Endpoint ---
@router.get("/me", response_model=schemas.User)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user

# --- Ticket Endpoints ---

@router.post("/tickets", response_model=schemas.Ticket, dependencies=[Depends(get_api_key)])
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    # Verify system exists
    system = db.query(models.System).filter(models.System.id == ticket.system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    new_ticket = models.Ticket(
        system_id=ticket.system_id,
        message=ticket.message,
        status="OPEN"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("/tickets", response_model=List[schemas.Ticket])
def get_tickets(skip: int = 0, limit: int = 100, status: Optional[str] = None, system_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Ticket)
    if status:
        query = query.filter(models.Ticket.status == status)
    if system_id:
        query = query.filter(models.Ticket.system_id == system_id)
    
    return query.order_by(models.Ticket.created_at.desc()).offset(skip).limit(limit).all()

@router.put("/tickets/{ticket_id}/status", response_model=schemas.Ticket)
def update_ticket_status(ticket_id: int, update: schemas.TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket.status = update.status
    
    if update.status == "RESOLVED" and not ticket.resolved_at:
        ticket.resolved_at = datetime.now(timezone.utc)
    elif update.status != "RESOLVED":
        ticket.resolved_at = None # Clear if reopened
        
    db.commit()
    db.refresh(ticket)
    return ticket
