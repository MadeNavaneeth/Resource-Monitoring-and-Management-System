"""
Populate database tables with sample data and display formatted results
"""
import sys
import os
from datetime import datetime, timedelta
from tabulate import tabulate

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.database import SessionLocal, engine, Base
from app.models.models import User, System, Alert, Metric, Ticket, AlertSettings
from app.core.security import get_password_hash

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"{title}")
    print("="*70)

def populate_users(db):
    """Populate users table"""
    print_section("1. Populating users Table")
    
    users_data = [
        {"email": "admin@resourcemonitor.com", "password": "admin123", "is_active": True},
        {"email": "nthy2355@gmail.com", "password": "password123", "is_active": True},
        {"email": "admin1@gmail.com", "password": "admin1pass", "is_active": True},
    ]
    
    print("\nINSERT Query:")
    print("""
INSERT INTO users (email, hashed_password, is_active) VALUES
('admin@resourcemonitor.com', '$hash1', 1),
('nthy2355@gmail.com', '$hash2', 1),
('admin1@gmail.com', '$hash3', 1);
    """)
    
    for user_data in users_data:
        user = User(
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
            is_active=user_data["is_active"]
        )
        db.add(user)
    
    db.commit()
    print(f"\nQuery OK, {len(users_data)} rows affected")
    
    # Verification
    print("\nVerification Query:")
    print("SELECT id, email, is_active, created_at FROM users;")
    
    users = db.query(User).all()
    table_data = [[u.id, u.email, u.is_active, u.created_at.strftime("%Y-%m-%d %H:%M:%S")] 
                  for u in users]
    print("\n" + tabulate(table_data, 
                          headers=["id", "email", "is_active", "created_at"],
                          tablefmt="grid"))

def populate_systems(db):
    """Populate systems table"""
    print_section("2. Populating systems Table")
    
    systems_data = [
        {
            "hostname": "DESKTOP-ABC123",
            "ip_address": "192.168.1.100",
            "mac_address": "00:1A:2B:3C:4D:5E",
            "os_info": "Windows 11 Pro",
            "os_build": "22621.3007",
            "windows_edition": "Professional",
            "cpu_name": "Intel Core i7-12700K",
            "cpu_cores": 12,
            "cpu_threads": 20,
            "architecture": "x64",
            "total_memory_gb": 32.0,
            "total_disk_gb": 512.0,
            "manufacturer": "Dell",
            "model": "OptiPlex 7090",
            "serial_number": "SN123456789",
            "username": "Admin",
            "is_active": True,
            "last_seen": datetime.now()
        },
        {
            "hostname": "LAB-SERVER-01",
            "ip_address": "192.168.1.101",
            "mac_address": "00:1A:2B:3C:4D:5F",
            "os_info": "Windows Server 2022",
            "os_build": "20348.2227",
            "windows_edition": "DataCenter",
            "cpu_name": "AMD Ryzen 9 5950X",
            "cpu_cores": 16,
            "cpu_threads": 32,
            "architecture": "x64",
            "total_memory_gb": 64.0,
            "total_disk_gb": 1024.0,
            "manufacturer": "HP",
            "model": "ProLiant DL380",
            "serial_number": "SN987654321",
            "username": "ServerAdmin",
            "is_active": True,
            "last_seen": datetime.now()
        },
        {
            "hostname": "WORKSTATION-02",
            "ip_address": "192.168.1.102",
            "mac_address": "00:1A:2B:3C:4D:60",
            "os_info": "Windows 10 Pro",
            "os_build": "19045.3803",
            "windows_edition": "Professional",
            "cpu_name": "Intel Core i5-11600",
            "cpu_cores": 6,
            "cpu_threads": 12,
            "architecture": "x64",
            "total_memory_gb": 16.0,
            "total_disk_gb": 256.0,
            "manufacturer": "Lenovo",
            "model": "ThinkCentre M70q",
            "serial_number": "SN456789123",
            "username": "User1",
            "is_active": True,
            "last_seen": datetime.now()
        }
    ]
    
    print("\nINSERT Query:")
    print("""
INSERT INTO systems (hostname, ip_address, mac_address, os_info, os_build, 
windows_edition, cpu_name, cpu_cores, cpu_threads, architecture, 
total_memory_gb, total_disk_gb, manufacturer, model, serial_number, 
username, is_active, last_seen) VALUES (...);
    """)
    
    for sys_data in systems_data:
        system = System(**sys_data)
        db.add(system)
    
    db.commit()
    print(f"\nQuery OK, {len(systems_data)} rows affected")
    
    # Verification
    print("\nVerification Query:")
    print("SELECT id, hostname, ip_address, os_info, cpu_name, total_memory_gb FROM systems;")
    
    systems = db.query(System).all()
    table_data = [[s.id, s.hostname, s.ip_address, s.os_info, s.cpu_name, s.total_memory_gb] 
                  for s in systems]
    print("\n" + tabulate(table_data, 
                          headers=["id", "hostname", "ip_address", "os_info", "cpu_name", "total_memory_gb"],
                          tablefmt="grid"))

def populate_alerts(db):
    """Populate alerts table"""
    print_section("3. Populating alerts Table")
    
    alerts_data = [
        {"system_id": 1, "alert_type": "CPU", "severity": "WARNING", 
         "message": "CPU usage exceeded 80% for 5 minutes", "is_resolved": False},
        {"system_id": 1, "alert_type": "MEMORY", "severity": "CRITICAL", 
         "message": "Memory usage at 95% - immediate action required", "is_resolved": False},
        {"system_id": 2, "alert_type": "DISK", "severity": "WARNING", 
         "message": "Disk usage at 85% on drive C:", "is_resolved": True},
        {"system_id": 3, "alert_type": "NETWORK", "severity": "INFO", 
         "message": "Network latency detected", "is_resolved": True},
    ]
    
    print("\nINSERT Query:")
    print("""
INSERT INTO alerts (system_id, alert_type, severity, message, is_resolved) VALUES
(1, 'CPU', 'WARNING', 'CPU usage exceeded 80% for 5 minutes', 0),
(1, 'MEMORY', 'CRITICAL', 'Memory usage at 95%...', 0),
(2, 'DISK', 'WARNING', 'Disk usage at 85% on drive C:', 1),
(3, 'NETWORK', 'INFO', 'Network latency detected', 1);
    """)
    
    for alert_data in alerts_data:
        alert = Alert(**alert_data)
        db.add(alert)
    
    db.commit()
    print(f"\nQuery OK, {len(alerts_data)} rows affected")
    
    # Verification
    print("\nVerification Query:")
    print("SELECT id, system_id, alert_type, severity, message, is_resolved FROM alerts;")
    
    alerts = db.query(Alert).all()
    table_data = [[a.id, a.system_id, a.alert_type, a.severity, 
                   a.message[:40] + "..." if len(a.message) > 40 else a.message, 
                   a.is_resolved] for a in alerts]
    print("\n" + tabulate(table_data, 
                          headers=["id", "system_id", "alert_type", "severity", "message", "is_resolved"],
                          tablefmt="grid"))

def populate_metrics(db):
    """Populate metrics table"""
    print_section("4. Populating metrics Table")
    
    metrics_data = [
        {"system_id": 1, "cpu_usage": 45.2, "memory_percent": 62.5, "memory_used": 20000000000,
         "disk_free": 230000000000, "disk_usage": 55.0, "disk_read_bytes": 150000000000,
         "disk_write_bytes": 98000000000, "network_sent": 45000000000, "network_recv": 32000000000,
         "process_count": 156, "uptime_seconds": 86400, "uptime_human": "1 day, 0:00:00"},
        {"system_id": 2, "cpu_usage": 28.7, "memory_percent": 48.3, "memory_used": 30000000000,
         "disk_free": 512000000000, "disk_usage": 50.0, "disk_read_bytes": 256000000000,
         "disk_write_bytes": 178000000000, "network_sent": 120000000000, "network_recv": 89000000000,
         "process_count": 203, "uptime_seconds": 172800, "uptime_human": "2 days, 0:00:00"},
        {"system_id": 3, "cpu_usage": 65.8, "memory_percent": 75.2, "memory_used": 12000000000,
         "disk_free": 128000000000, "disk_usage": 50.0, "disk_read_bytes": 89000000000,
         "disk_write_bytes": 45000000000, "network_sent": 23000000000, "network_recv": 18000000000,
         "process_count": 98, "uptime_seconds": 43200, "uptime_human": "12 hours, 0:00:00"},
    ]
    
    print("\nINSERT Query:")
    print("""
INSERT INTO metrics (system_id, cpu_usage, memory_percent, memory_used,
disk_free, disk_usage, process_count, uptime_seconds, uptime_human) VALUES
(1, 45.2, 62.5, 20000000000, 230000000000, 55.0, 156, 86400, '1 day, 0:00:00'),
(...);
    """)
    
    for metric_data in metrics_data:
        metric = Metric(**metric_data)
        db.add(metric)
    
    db.commit()
    print(f"\nQuery OK, {len(metrics_data)} rows affected")
    
    # Verification
    print("\nVerification Query:")
    print("SELECT id, system_id, cpu_usage, memory_percent, disk_usage, process_count, uptime_human FROM metrics;")
    
    metrics = db.query(Metric).all()
    table_data = [[m.id, m.system_id, m.cpu_usage, m.memory_percent, 
                   m.disk_usage, m.process_count, m.uptime_human] for m in metrics]
    print("\n" + tabulate(table_data, 
                          headers=["id", "system_id", "cpu_usage", "memory_percent", 
                                   "disk_usage", "process_count", "uptime_human"],
                          tablefmt="grid"))

def populate_tickets(db):
    """Populate tickets table"""
    print_section("5. Populating tickets Table")
    
    tickets_data = [
        {"system_id": 1, "message": "System running slow - needs investigation", 
         "status": "OPEN", "resolved_at": None},
        {"system_id": 2, "message": "Disk cleanup required on C: drive", 
         "status": "RESOLVED", "resolved_at": datetime.now() - timedelta(days=1)},
        {"system_id": 3, "message": "Software update needed for antivirus", 
         "status": "OPEN", "resolved_at": None},
        {"system_id": 1, "message": "Network adapter driver issue", 
         "status": "RESOLVED", "resolved_at": datetime.now() - timedelta(days=2)},
    ]
    
    print("\nINSERT Query:")
    print("""
INSERT INTO tickets (system_id, message, status, resolved_at) VALUES
(1, 'System running slow - needs investigation', 'OPEN', NULL),
(2, 'Disk cleanup required on C: drive', 'RESOLVED', '2025-12-27 14:30:00'),
(...);
    """)
    
    for ticket_data in tickets_data:
        ticket = Ticket(**ticket_data)
        db.add(ticket)
    
    db.commit()
    print(f"\nQuery OK, {len(tickets_data)} rows affected")
    
    # Verification
    print("\nVerification Query:")
    print("SELECT id, system_id, message, status, created_at, resolved_at FROM tickets;")
    
    tickets = db.query(Ticket).all()
    table_data = [[t.id, t.system_id, t.message[:40] + "..." if len(t.message) > 40 else t.message, 
                   t.status, t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                   t.resolved_at.strftime("%Y-%m-%d %H:%M:%S") if t.resolved_at else "NULL"] 
                  for t in tickets]
    print("\n" + tabulate(table_data, 
                          headers=["id", "system_id", "message", "status", "created_at", "resolved_at"],
                          tablefmt="grid"))

def populate_alert_settings(db):
    """Populate alert_settings table"""
    print_section("6. Populating alert_settings Table")
    
    settings_data = [
        {"system_id": 1, "cpu_threshold": 85.0, "memory_threshold": 90.0, "disk_threshold": 85.0},
        {"system_id": 2, "cpu_threshold": 80.0, "memory_threshold": 85.0, "disk_threshold": 80.0},
        {"system_id": 3, "cpu_threshold": 90.0, "memory_threshold": 90.0, "disk_threshold": 90.0},
        {"system_id": None, "cpu_threshold": 90.0, "memory_threshold": 90.0, "disk_threshold": 90.0},
    ]
    
    print("\nINSERT Query:")
    print("""
INSERT INTO alert_settings (system_id, cpu_threshold, memory_threshold, disk_threshold) VALUES
(1, 85.0, 90.0, 85.0),
(2, 80.0, 85.0, 80.0),
(3, 90.0, 90.0, 90.0),
(NULL, 90.0, 90.0, 90.0);
    """)
    
    for setting_data in settings_data:
        setting = AlertSettings(**setting_data)
        db.add(setting)
    
    db.commit()
    print(f"\nQuery OK, {len(settings_data)} rows affected")
    
    # Verification
    print("\nVerification Query:")
    print("SELECT id, system_id, cpu_threshold, memory_threshold, disk_threshold FROM alert_settings;")
    
    settings = db.query(AlertSettings).all()
    table_data = [[s.id, s.system_id if s.system_id else "NULL", 
                   s.cpu_threshold, s.memory_threshold, s.disk_threshold] for s in settings]
    print("\n" + tabulate(table_data, 
                          headers=["id", "system_id", "cpu_threshold", "memory_threshold", "disk_threshold"],
                          tablefmt="grid"))

def main():
    """Main function to populate all tables"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  DATABASE POPULATION - Resource Monitoring System".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Populate each table
        populate_users(db)
        populate_systems(db)
        populate_alerts(db)
        populate_metrics(db)
        populate_tickets(db)
        populate_alert_settings(db)
        
        # Summary
        print_section("DATABASE POPULATION SUMMARY")
        print("\nVerification Summary Query:")
        print("""
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL SELECT 'systems', COUNT(*) FROM systems
UNION ALL SELECT 'alerts', COUNT(*) FROM alerts
UNION ALL SELECT 'metrics', COUNT(*) FROM metrics
UNION ALL SELECT 'tickets', COUNT(*) FROM tickets
UNION ALL SELECT 'alert_settings', COUNT(*) FROM alert_settings;
        """)
        
        summary_data = [
            ["users", db.query(User).count()],
            ["systems", db.query(System).count()],
            ["alerts", db.query(Alert).count()],
            ["metrics", db.query(Metric).count()],
            ["tickets", db.query(Ticket).count()],
            ["alert_settings", db.query(AlertSettings).count()],
        ]
        
        print("\n" + tabulate(summary_data, 
                              headers=["table_name", "row_count"],
                              tablefmt="grid"))
        
        print("\n" + "="*70)
        print("✅ All tables populated successfully!")
        print("="*70)
        print("\nYou can now take screenshots of the output above.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
