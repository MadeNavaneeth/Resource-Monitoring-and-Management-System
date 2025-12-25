from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime, timezone

# --- User/Auth Schemas ---

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    is_active: bool

# --- System Schemas ---

class SystemBase(BaseModel):
    hostname: str
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os_info: Optional[str] = None
    os_build: Optional[str] = None
    windows_edition: Optional[str] = None
    user_label: Optional[str] = None
    agent_version: Optional[str] = None
    cpu_name: Optional[str] = None
    cpu_cores: Optional[int] = None
    cpu_threads: Optional[int] = None
    architecture: Optional[str] = None
    total_memory_gb: Optional[float] = None
    total_disk_gb: Optional[float] = None
    disk_model: Optional[str] = None
    gpu_name: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    bios_version: Optional[str] = None
    username: Optional[str] = None
    domain: Optional[str] = None
    timezone: Optional[str] = None
    network_adapter: Optional[str] = None
    battery_percent: Optional[float] = None
    is_plugged_in: Optional[bool] = None
    python_version: Optional[str] = None
    drivers: Optional[List[Any]] = None

class SystemCreate(SystemBase):
    pass

class SystemUpdate(BaseModel):
    ip_address: Optional[str] = None
    os_info: Optional[str] = None
    agent_version: Optional[str] = None
    is_active: Optional[bool] = None
    last_seen: Optional[datetime] = None

class System(SystemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    last_seen: Optional[datetime] = None
    created_at: datetime

# --- Metric Schemas ---

class MetricBase(BaseModel):
    system_id: int
    cpu_usage: float
    cpu_per_core: Optional[List[float]] = None
    memory_total: int
    memory_used: int
    memory_available: Optional[int] = None
    memory_percent: Optional[float] = None
    swap_total: Optional[int] = None
    swap_used: Optional[int] = None
    swap_percent: Optional[float] = None
    disk_total: Optional[int] = None
    disk_used: Optional[int] = None
    disk_free: Optional[int] = None
    disk_usage: float
    disk_read_bytes: Optional[int] = 0
    disk_write_bytes: Optional[int] = 0
    network_sent: int
    network_recv: int
    network_packets_sent: Optional[int] = None
    network_packets_recv: Optional[int] = None
    process_count: Optional[int] = None
    boot_time: Optional[str] = None
    uptime_seconds: Optional[int] = None
    uptime_human: Optional[str] = None
    top_processes: Optional[List[Any]] = None
    timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class MetricCreate(MetricBase):
    pass

class Metric(MetricBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# --- Alert Schemas ---

class AlertBase(BaseModel):
    system_id: int
    alert_type: str
    severity: str
    message: str

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_resolved: bool
    created_at: datetime

# --- Ticket Schemas ---

class TicketBase(BaseModel):
    system_id: int
    message: str

class TicketCreate(TicketBase):
    message: str = Field(..., max_length=500, min_length=5)

class TicketUpdate(BaseModel):
    status: str

class Ticket(TicketBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    resolved_at: Optional[datetime] = None
    created_at: datetime

# --- Alert Settings Schemas ---

class AlertSettingsBase(BaseModel):
    system_id: Optional[int] = None
    cpu_threshold: float
    memory_threshold: float
    disk_threshold: float

class AlertSettingsCreate(AlertSettingsBase):
    pass

class AlertSettings(AlertSettingsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
