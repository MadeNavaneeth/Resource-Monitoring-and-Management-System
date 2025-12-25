from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, JSON, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class System(Base):
    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, unique=True, index=True, nullable=False)
    ip_address = Column(String, nullable=True)
    mac_address = Column(String, nullable=True)
    os_info = Column(String, nullable=True)
    os_build = Column(String, nullable=True)
    windows_edition = Column(String, nullable=True)
    user_label = Column(String, nullable=True)
    agent_version = Column(String, nullable=True)
    cpu_name = Column(String, nullable=True)
    cpu_cores = Column(Integer, nullable=True)
    cpu_threads = Column(Integer, nullable=True)
    architecture = Column(String, nullable=True)
    total_memory_gb = Column(Float, nullable=True)
    total_disk_gb = Column(Float, nullable=True)
    disk_model = Column(String, nullable=True)
    gpu_name = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    bios_version = Column(String, nullable=True)
    username = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    network_adapter = Column(String, nullable=True)
    battery_percent = Column(Float, nullable=True)
    is_plugged_in = Column(Boolean, nullable=True)
    python_version = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    drivers = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    alerts = relationship("Alert", back_populates="system", cascade="all, delete-orphan")
    metrics = relationship("Metric", back_populates="system", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="system", cascade="all, delete-orphan")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    system = relationship("System", back_populates="alerts")

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    cpu_usage = Column(Float)
    memory_percent = Column(Float)
    memory_used = Column(BigInteger) # Added for tracking used memory bytes
    disk_free = Column(BigInteger)
    disk_usage = Column(Float)
    
    # Disk I/O (Cumulative Bytes)
    disk_read_bytes = Column(BigInteger, default=0)
    disk_write_bytes = Column(BigInteger, default=0)

    # Network
    network_sent = Column(BigInteger)
    network_recv = Column(Float)
    process_count = Column(Integer)
    boot_time = Column(String, nullable=True)
    uptime_seconds = Column(Integer, nullable=True)
    uptime_human = Column(String, nullable=True)
    top_processes = Column(JSON, nullable=True)

    system = relationship("System", back_populates="metrics")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    message = Column(String, nullable=False)
    status = Column(String, default="OPEN") # OPEN, RESOLVED
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    system = relationship("System", back_populates="tickets")

class AlertSettings(Base):
    __tablename__ = "alert_settings"

    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"), nullable=True)
    cpu_threshold = Column(Float, default=90.0)
    memory_threshold = Column(Float, default=90.0)
    disk_threshold = Column(Float, default=90.0)

    system = relationship("System")
