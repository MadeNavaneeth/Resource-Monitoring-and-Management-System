RV College of Engineering®, Bengaluru – 59
Department of Information Science and Engineering
Database Management Systems (CD252IA)

Mid-Term Report on Database Project

TITLE: RESOURCE MONITORING AND MANAGEMENT SYSTEM

TEAM
USN: [Your USN]          [Your Name]
USN: [Team Member USN]   [Team Member Name]

================================================================================

1. Tables Created Details

Our project database has been designed using normalization principles to ensure data 
integrity and reduce redundancy. It consists of six related tables that work together 
to provide comprehensive system monitoring and management capabilities.

1.1 users
Purpose: Manages administrator accounts and serves as the root entity for authentication.
Attributes:
  - id (PK): INTEGER, Primary key, auto-increment
  - email: VARCHAR, Unique identifier for each user
  - hashed_password: VARCHAR, Securely hashed password (PBKDF2-SHA256)
  - is_active: BOOLEAN, Account status flag (default: TRUE)
  - created_at: DATETIME, Timestamp of account creation

1.2 systems
Purpose: The central entity storing comprehensive information about each monitored 
computer system. This table maintains both static hardware information and dynamic 
system state.

Attributes:
  - id (PK): INTEGER, Primary key, auto-increment
  - hostname: VARCHAR, Unique system identifier
  - ip_address: VARCHAR, Network IP address
  - mac_address: VARCHAR, Physical network adapter address
  - os_info: VARCHAR, Operating system information
  - os_build: VARCHAR, OS build number
  - windows_edition: VARCHAR, Windows edition (e.g., Pro, Enterprise)
  - user_label: VARCHAR, Custom label for the system
  - agent_version: VARCHAR, Version of the monitoring agent
  - cpu_name: VARCHAR, Processor model name
  - cpu_cores: INTEGER, Number of physical CPU cores
  - cpu_threads: INTEGER, Number of logical processors
  - architecture: VARCHAR, System architecture (x64, x86)
  - total_memory_gb: FLOAT, Total RAM in gigabytes
  - total_disk_gb: FLOAT, Total storage capacity
  - disk_model: VARCHAR, Storage device model
  - gpu_name: VARCHAR, Graphics card name
  - manufacturer: VARCHAR, System manufacturer (Dell, HP, etc.)
  - model: VARCHAR, System model number
  - serial_number: VARCHAR, Hardware serial number
  - bios_version: VARCHAR, BIOS/UEFI version
  - username: VARCHAR, Current logged-in user
  - domain: VARCHAR, Windows domain (if applicable)
  - timezone: VARCHAR, System timezone
  - network_adapter: VARCHAR, Primary network adapter
  - battery_percent: FLOAT, Battery percentage (for laptops)
  - is_plugged_in: BOOLEAN, Power adapter status
  - python_version: VARCHAR, Python version on system
  - is_active: BOOLEAN, System active status
  - last_seen: DATETIME, Last communication timestamp
  - drivers: JSON, List of installed drivers
  - created_at: DATETIME, First registration timestamp

1.3 metrics
Purpose: Stores time-series performance data collected from monitored systems. Each 
row represents a snapshot of system performance at a specific point in time.

Attributes:
  - id (PK): INTEGER, Primary key, auto-increment
  - system_id (FK): INTEGER, References systems(id)
  - timestamp: DATETIME, Metric collection time (indexed)
  - cpu_usage: FLOAT, CPU utilization percentage
  - memory_percent: FLOAT, RAM usage percentage
  - memory_used: BIGINT, RAM used in bytes
  - disk_free: BIGINT, Available disk space in bytes
  - disk_usage: FLOAT, Disk utilization percentage
  - disk_read_bytes: BIGINT, Cumulative disk read bytes
  - disk_write_bytes: BIGINT, Cumulative disk write bytes
  - network_sent: BIGINT, Network bytes sent
  - network_recv: FLOAT, Network bytes received
  - process_count: INTEGER, Number of running processes
  - boot_time: VARCHAR, System boot timestamp
  - uptime_seconds: INTEGER, System uptime in seconds
  - uptime_human: VARCHAR, Human-readable uptime
  - top_processes: JSON, List of resource-intensive processes

1.4 alerts
Purpose: Stores system alerts triggered when performance metrics exceed configured 
thresholds. Provides alert history and resolution tracking.

Attributes:
  - id (PK): INTEGER, Primary key, auto-increment
  - system_id (FK): INTEGER, References systems(id)
  - alert_type: VARCHAR, Type of alert (CPU, Memory, Disk)
  - severity: VARCHAR, Alert severity level (Warning, Critical)
  - message: VARCHAR, Detailed alert message
  - is_resolved: BOOLEAN, Resolution status (default: FALSE)
  - created_at: DATETIME, Alert creation timestamp

1.5 tickets
Purpose: Stores support tickets created for system issues. Provides issue tracking 
and resolution management.

Attributes:
  - id (PK): INTEGER, Primary key, auto-increment
  - system_id (FK): INTEGER, References systems(id)
  - message: VARCHAR, Ticket description
  - status: VARCHAR, Ticket status (OPEN, RESOLVED)
  - resolved_at: DATETIME, Resolution timestamp (nullable)
  - created_at: DATETIME, Ticket creation timestamp

1.6 alert_settings
Purpose: Stores configurable alert thresholds for monitored systems. Allows per-system 
or global threshold configuration.

Attributes:
  - id (PK): INTEGER, Primary key, auto-increment
  - system_id (FK): INTEGER, References systems(id), nullable for global settings
  - cpu_threshold: FLOAT, CPU usage alert threshold (default: 90.0)
  - memory_threshold: FLOAT, Memory usage alert threshold (default: 90.0)
  - disk_threshold: FLOAT, Disk usage alert threshold (default: 90.0)

================================================================================

2. Table Creation Queries

The following SQLite DDL queries are used to create the complete, normalized database 
schema. The order of creation is important due to the foreign key dependencies.

-- 1. Create the 'users' table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the 'systems' table
CREATE TABLE systems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname VARCHAR UNIQUE NOT NULL,
    ip_address VARCHAR,
    mac_address VARCHAR,
    os_info VARCHAR,
    os_build VARCHAR,
    windows_edition VARCHAR,
    user_label VARCHAR,
    agent_version VARCHAR,
    cpu_name VARCHAR,
    cpu_cores INTEGER,
    cpu_threads INTEGER,
    architecture VARCHAR,
    total_memory_gb FLOAT,
    total_disk_gb FLOAT,
    disk_model VARCHAR,
    gpu_name VARCHAR,
    manufacturer VARCHAR,
    model VARCHAR,
    serial_number VARCHAR,
    bios_version VARCHAR,
    username VARCHAR,
    domain VARCHAR,
    timezone VARCHAR,
    network_adapter VARCHAR,
    battery_percent FLOAT,
    is_plugged_in BOOLEAN,
    python_version VARCHAR,
    is_active BOOLEAN DEFAULT 1,
    last_seen DATETIME,
    drivers JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create the 'metrics' table with foreign key to systems
CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_usage FLOAT,
    memory_percent FLOAT,
    memory_used BIGINT,
    disk_free BIGINT,
    disk_usage FLOAT,
    disk_read_bytes BIGINT DEFAULT 0,
    disk_write_bytes BIGINT DEFAULT 0,
    network_sent BIGINT,
    network_recv FLOAT,
    process_count INTEGER,
    boot_time VARCHAR,
    uptime_seconds INTEGER,
    uptime_human VARCHAR,
    top_processes JSON,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
);

-- Create index on timestamp for faster time-series queries
CREATE INDEX idx_metrics_timestamp ON metrics(timestamp);
CREATE INDEX idx_metrics_system_id ON metrics(system_id);

-- 4. Create the 'alerts' table with foreign key to systems
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id INTEGER NOT NULL,
    alert_type VARCHAR NOT NULL,
    severity VARCHAR NOT NULL,
    message VARCHAR NOT NULL,
    is_resolved BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
);

-- Create index for faster alert queries
CREATE INDEX idx_alerts_system_id ON alerts(system_id);
CREATE INDEX idx_alerts_resolved ON alerts(is_resolved);

-- 5. Create the 'tickets' table with foreign key to systems
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id INTEGER NOT NULL,
    message VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'OPEN',
    resolved_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
);

-- Create index for faster ticket queries
CREATE INDEX idx_tickets_system_id ON tickets(system_id);
CREATE INDEX idx_tickets_status ON tickets(status);

-- 6. Create the 'alert_settings' table with optional foreign key to systems
CREATE TABLE alert_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id INTEGER,
    cpu_threshold FLOAT DEFAULT 90.0,
    memory_threshold FLOAT DEFAULT 90.0,
    disk_threshold FLOAT DEFAULT 90.0,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
);

================================================================================

3. Table Population Queries

The following SQL INSERT statements demonstrate how to populate the database with 
sample data.

-- 1. Populate 'users' (passwords are hashed using PBKDF2-SHA256)
INSERT INTO users (email, hashed_password, is_active) VALUES
('admin@resourcemonitor.com', '$pbkdf2-sha256$29000$WKv1nhOCMOa8V4oxhrD2fg$gnP1ywh...', 1),
('nthy2355@gmail.com', '$pbkdf2-sha256$29000$WKv1nhOCMOa8V4oxhrD2fg$gnP1ywh...', 1),
('Admin1@gmail.com', '$pbkdf2-sha256$29000$GmOM0boXolSq9Z4zplTqHQ$ZXi4ynMp...', 1);

-- 2. Populate 'systems' with monitored computer information
INSERT INTO systems (
    hostname, ip_address, mac_address, os_info, windows_edition,
    cpu_name, cpu_cores, cpu_threads, total_memory_gb, manufacturer,
    model, is_active, last_seen
) VALUES
(
    'DESKTOP-ABC123',
    '192.168.1.100',
    '00:1A:2B:3C:4D:5E',
    'Windows 11 Pro',
    'Professional',
    'Intel Core i7-12700K',
    12,
    20,
    32.0,
    'Dell',
    'OptiPlex 7090',
    1,
    CURRENT_TIMESTAMP
),
(
    'LAPTOP-XYZ789',
    '192.168.1.101',
    'AA:BB:CC:DD:EE:FF',
    'Windows 10 Pro',
    'Professional',
    'AMD Ryzen 7 5800H',
    8,
    16,
    16.0,
    'HP',
    'EliteBook 840',
    1,
    CURRENT_TIMESTAMP
),
(
    'WORKSTATION-MNO456',
    '192.168.1.102',
    '11:22:33:44:55:66',
    'Windows 11 Enterprise',
    'Enterprise',
    'Intel Xeon W-2295',
    18,
    36,
    64.0,
    'Lenovo',
    'ThinkStation P620',
    1,
    CURRENT_TIMESTAMP
);

-- 3. Populate 'metrics' with performance data snapshots
-- Assuming system_ids are 1, 2, and 3
INSERT INTO metrics (
    system_id, cpu_usage, memory_percent, memory_used, disk_usage, 
    disk_free, network_sent, network_recv, process_count, uptime_seconds
) VALUES
-- Metrics for DESKTOP-ABC123
(1, 45.2, 62.5, 21474836480, 55.0, 242949672960, 1073741824, 2147483648, 156, 86400),
(1, 52.8, 68.3, 23622320128, 55.1, 242415624192, 1181116006, 2361835520, 162, 90000),
(1, 38.5, 59.1, 20401094656, 55.2, 241881575424, 1288490188, 2576187392, 151, 93600),

-- Metrics for LAPTOP-XYZ789
(2, 28.3, 45.7, 7851769856, 72.0, 76293945344, 536870912, 1073741824, 98, 43200),
(2, 35.1, 52.4, 9006399488, 72.5, 74901094400, 590558003, 1181116006, 105, 46800),
(2, 41.2, 58.9, 10124115968, 73.0, 73508243456, 644245094, 1288490188, 112, 50400),

-- Metrics for WORKSTATION-MNO456
(3, 72.5, 81.2, 55834574848, 45.0, 603979776000, 2147483648, 4294967296, 245, 172800),
(3, 68.9, 78.5, 53959524352, 45.3, 602060800000, 2361835520, 4723056640, 238, 176400),
(3, 75.2, 84.1, 57843122176, 45.6, 600141824000, 2576187392, 5151146086, 252, 180000);

-- 4. Populate 'alerts' for systems exceeding thresholds
INSERT INTO alerts (system_id, alert_type, severity, message, is_resolved) VALUES
(3, 'CPU', 'Warning', 'CPU usage at 72.5% - approaching threshold', 0),
(3, 'Memory', 'Warning', 'Memory usage at 81.2% - approaching threshold', 0),
(2, 'Disk', 'Warning', 'Disk usage at 72% - approaching threshold', 0),
(1, 'CPU', 'Warning', 'CPU spike detected - 52.8% usage', 1);

-- 5. Populate 'tickets' for system issues
INSERT INTO tickets (system_id, message, status, resolved_at) VALUES
(3, 'High CPU usage reported by monitoring agent. Investigate background processes.', 'OPEN', NULL),
(2, 'Disk space running low. Need to clean up temporary files or upgrade storage.', 'OPEN', NULL),
(1, 'Temporary CPU spike resolved. Caused by Windows Update process.', 'RESOLVED', CURRENT_TIMESTAMP);

-- 6. Populate 'alert_settings' with custom thresholds
INSERT INTO alert_settings (system_id, cpu_threshold, memory_threshold, disk_threshold) VALUES
-- Global default settings
(NULL, 90.0, 90.0, 90.0),
-- Custom settings for WORKSTATION (lower thresholds for critical system)
(3, 70.0, 80.0, 85.0),
-- Custom settings for LAPTOP (higher disk threshold)
(2, 90.0, 90.0, 80.0);

================================================================================

4. Query Execution for Data Retrieval

The following are 5 examples of essential SELECT queries that leverage the normalized 
schema and demonstrate the power of relational database design.

4.1 Fetch All Active Systems with Their Latest Status

Purpose: To display a comprehensive list of all monitored systems with their most 
recent performance metrics for the dashboard overview.

Query:
SELECT 
    s.id,
    s.hostname,
    s.ip_address,
    s.os_info,
    s.cpu_name,
    s.total_memory_gb,
    s.is_active,
    s.last_seen,
    m.cpu_usage AS latest_cpu,
    m.memory_percent AS latest_memory,
    m.disk_usage AS latest_disk
FROM systems s
LEFT JOIN (
    SELECT 
        system_id,
        cpu_usage,
        memory_percent,
        disk_usage,
        ROW_NUMBER() OVER (PARTITION BY system_id ORDER BY timestamp DESC) AS rn
    FROM metrics
) m ON s.id = m.system_id AND m.rn = 1
WHERE s.is_active = 1
ORDER BY s.hostname;

Sample Output:
id | hostname           | ip_address    | latest_cpu | latest_memory | latest_disk
---|-------------------|---------------|------------|---------------|-------------
1  | DESKTOP-ABC123    | 192.168.1.100 | 38.5       | 59.1          | 55.2
2  | LAPTOP-XYZ789     | 192.168.1.101 | 41.2       | 58.9          | 73.0
3  | WORKSTATION-MNO456| 192.168.1.102 | 75.2       | 84.1          | 45.6


4.2 Fetch Detailed System Information with Hardware Specifications

Purpose: To display complete hardware and software details for a specific system, 
useful for the system detail page.

Query:
SELECT 
    s.hostname,
    s.ip_address,
    s.mac_address,
    s.os_info,
    s.windows_edition,
    s.cpu_name,
    s.cpu_cores,
    s.cpu_threads,
    s.architecture,
    s.total_memory_gb,
    s.total_disk_gb,
    s.disk_model,
    s.gpu_name,
    s.manufacturer,
    s.model,
    s.serial_number,
    s.bios_version,
    s.last_seen,
    COUNT(DISTINCT a.id) AS total_alerts,
    COUNT(DISTINCT t.id) AS open_tickets
FROM systems s
LEFT JOIN alerts a ON s.id = a.system_id AND a.is_resolved = 0
LEFT JOIN tickets t ON s.id = t.system_id AND t.status = 'OPEN'
WHERE s.hostname = 'WORKSTATION-MNO456'
GROUP BY s.id;

Sample Output:
hostname: WORKSTATION-MNO456
cpu_name: Intel Xeon W-2295
cpu_cores: 18
total_memory_gb: 64.0
total_alerts: 2
open_tickets: 1


4.3 Calculate Average CPU and Memory Usage Over Last 24 Hours

Purpose: To generate performance trend analysis for monitoring system health over time.

Query:
SELECT 
    s.hostname,
    ROUND(AVG(m.cpu_usage), 2) AS avg_cpu,
    ROUND(AVG(m.memory_percent), 2) AS avg_memory,
    ROUND(MAX(m.cpu_usage), 2) AS peak_cpu,
    ROUND(MAX(m.memory_percent), 2) AS peak_memory,
    COUNT(m.id) AS sample_count
FROM systems s
JOIN metrics m ON s.id = m.system_id
WHERE m.timestamp >= datetime('now', '-1 day')
GROUP BY s.id, s.hostname
ORDER BY avg_cpu DESC;

Sample Output:
hostname           | avg_cpu | avg_memory | peak_cpu | peak_memory | sample_count
-------------------|---------|------------|----------|-------------|-------------
WORKSTATION-MNO456 | 72.20   | 81.27      | 75.20    | 84.10       | 288
DESKTOP-ABC123     | 45.50   | 63.30      | 52.80    | 68.30       | 288
LAPTOP-XYZ789      | 34.87   | 52.33      | 41.20    | 58.90       | 288


4.4 Find All Systems with Active Alerts and Alert Details

Purpose: To display a comprehensive alert dashboard showing all unresolved issues 
across the infrastructure.

Query:
SELECT 
    s.hostname,
    s.ip_address,
    a.alert_type,
    a.severity,
    a.message,
    a.created_at,
    ast.cpu_threshold,
    ast.memory_threshold,
    ast.disk_threshold
FROM systems s
JOIN alerts a ON s.id = a.system_id
LEFT JOIN alert_settings ast ON s.id = ast.system_id
WHERE a.is_resolved = 0
ORDER BY a.severity DESC, a.created_at DESC;

Sample Output:
hostname           | alert_type | severity | message                          | created_at
-------------------|------------|----------|----------------------------------|-------------------
WORKSTATION-MNO456 | Memory     | Warning  | Memory usage at 81.2% - approaching... | 2025-12-27 10:30
WORKSTATION-MNO456 | CPU        | Warning  | CPU usage at 72.5% - approaching...    | 2025-12-27 10:25
LAPTOP-XYZ789      | Disk       | Warning  | Disk usage at 72% - approaching...     | 2025-12-27 09:15


4.5 Generate Comprehensive System Health Report with Metrics and Tickets

Purpose: A complex query combining multiple tables for an advanced management report, 
showing systems that need attention.

Query:
SELECT 
    s.hostname,
    s.manufacturer,
    s.model,
    s.last_seen,
    ROUND(AVG(m.cpu_usage), 2) AS avg_cpu_24h,
    ROUND(AVG(m.memory_percent), 2) AS avg_memory_24h,
    COUNT(DISTINCT a.id) AS unresolved_alerts,
    COUNT(DISTINCT t.id) AS open_tickets,
    GROUP_CONCAT(DISTINCT a.alert_type) AS alert_types,
    CASE 
        WHEN COUNT(DISTINCT a.id) > 2 THEN 'CRITICAL'
        WHEN COUNT(DISTINCT a.id) > 0 THEN 'WARNING'
        ELSE 'HEALTHY'
    END AS health_status
FROM systems s
LEFT JOIN metrics m ON s.id = m.system_id 
    AND m.timestamp >= datetime('now', '-1 day')
LEFT JOIN alerts a ON s.id = a.system_id 
    AND a.is_resolved = 0
LEFT JOIN tickets t ON s.id = t.system_id 
    AND t.status = 'OPEN'
WHERE s.is_active = 1
GROUP BY s.id, s.hostname, s.manufacturer, s.model, s.last_seen
HAVING unresolved_alerts > 0 OR open_tickets > 0
ORDER BY unresolved_alerts DESC, avg_cpu_24h DESC;

Sample Output:
hostname      | avg_cpu_24h | avg_memory_24h | unresolved_alerts | alert_types  | health_status
--------------|-------------|----------------|-------------------|--------------|---------------
WORKSTATION   | 72.20       | 81.27          | 2                 | CPU,Memory   | CRITICAL
LAPTOP-XYZ789 | 34.87       | 52.33          | 1                 | Disk         | WARNING

================================================================================

5. Database Relationships and Normalization

5.1 Foreign Key Relationships

The database implements the following foreign key relationships with CASCADE deletion 
to maintain referential integrity:

1. metrics.system_id → systems.id (ON DELETE CASCADE)
   - When a system is deleted, all its metrics are automatically removed
   
2. alerts.system_id → systems.id (ON DELETE CASCADE)
   - When a system is deleted, all its alerts are automatically removed
   
3. tickets.system_id → systems.id (ON DELETE CASCADE)
   - When a system is deleted, all its tickets are automatically removed
   
4. alert_settings.system_id → systems.id (ON DELETE CASCADE)
   - When a system is deleted, its custom alert settings are removed

5.2 Normalization Level

The database schema follows Third Normal Form (3NF):

- First Normal Form (1NF): All attributes contain atomic values
- Second Normal Form (2NF): No partial dependencies on composite keys
- Third Normal Form (3NF): No transitive dependencies

Special Cases:
- JSON fields (drivers, top_processes) are used for flexible data that doesn't 
  warrant separate tables
- Time-series metrics table optimized for write performance

5.3 Indexes for Performance

Strategic indexes have been created to optimize query performance:

- metrics(timestamp): For time-range queries
- metrics(system_id): For system-specific metric retrieval
- alerts(system_id, is_resolved): For alert dashboard queries
- tickets(system_id, status): For ticket management queries
- systems(hostname): For unique constraint and fast lookups

================================================================================

6. Database File Location and Verification

Database File: backend/resource_monitor.db
Database Type: SQLite 3
Current Size: ~256 KB
Total Tables: 6

Verification Commands:
# View database structure
sqlite3 backend/resource_monitor.db ".schema"

# Count records in each table
sqlite3 backend/resource_monitor.db "SELECT 'users', COUNT(*) FROM users 
UNION SELECT 'systems', COUNT(*) FROM systems 
UNION SELECT 'metrics', COUNT(*) FROM metrics;"

# View all users
python inspect_db.py

# View detailed information
python view_all_user_data.py

================================================================================

7. Security Implementation

7.1 Password Security
- All passwords are hashed using PBKDF2-SHA256 algorithm
- 29,000 iterations for strong key derivation
- Passwords are never stored in plain text
- Implemented via passlib library in backend/app/core/security.py

7.2 Data Validation
- Backend validation using Pydantic schemas
- Type checking for all API inputs
- SQL injection prevention through SQLAlchemy ORM
- Foreign key constraints enforce referential integrity

7.3 Authentication
- JWT-based authentication for API access
- Token expiration and validation
- Protected endpoints require valid authentication

================================================================================

Conclusion

This database design provides a robust, scalable foundation for the Resource Monitoring 
and Management System. The normalized schema ensures data integrity, the foreign key 
relationships maintain referential consistency, and the strategic indexing provides 
optimal query performance for real-time monitoring scenarios.

The database successfully supports:
✓ Multi-user authentication
✓ Comprehensive system tracking
✓ Time-series performance metrics
✓ Automated alert generation
✓ Ticket management
✓ Configurable thresholds
✓ Complex analytical queries
✓ Data integrity through cascade deletion
