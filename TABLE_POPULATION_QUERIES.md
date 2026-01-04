# Table Population Queries - Resource Monitoring and Management System

## 1. Populate users Table

**Query:**

```sql
INSERT INTO users (email, hashed_password, is_active) VALUES
('admin@resourcemonitor.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8J9z1K2vY3mQ4pL5wZy', 1),
('nthy2355@gmail.com', '$2b$12$8kF2xN9pW1mH3jK5vL7qXeYzP4tR6sW8uV0mN2kJ3hL9gF5dC1aB', 1),
('admin1@gmail.com', '$2b$12$3mT4nU5vK6wL7xM8yN9zA0P1qR2sT3uV4wX5yZ6aC7bD8eF9gH0i', 1);
```

**Output:**

```
Query OK, 3 rows affected
```

**Verification Query:**

```sql
SELECT id, email, is_active, created_at FROM users;
```

**Output:**

```
+----+---------------------------+-----------+---------------------+
| id | email                     | is_active | created_at          |
+----+---------------------------+-----------+---------------------+
| 1  | admin@resourcemonitor.com | 1         | 2025-12-28 13:25:00 |
| 2  | nthy2355@gmail.com        | 1         | 2025-12-28 13:25:00 |
| 3  | admin1@gmail.com          | 1         | 2025-12-28 13:25:00 |
+----+---------------------------+-----------+---------------------+
```

---

## 2. Populate systems Table

**Query:**

```sql
INSERT INTO systems (hostname, ip_address, mac_address, os_info,
os_build, windows_edition, cpu_name, cpu_cores, cpu_threads,
architecture, total_memory_gb, total_disk_gb, manufacturer, model,
serial_number, username, is_active, last_seen)
VALUES 
('DESKTOP-ABC123', '192.168.1.100', '00:1A:2B:3C:4D:5E', 'Windows 11 Pro',
'22621.3007', 'Professional', 'Intel Core i7-12700K', 12, 20,
'x64', 32.0, 512.0, 'Dell', 'OptiPlex 7090', 'SN123456789',
'Admin', 1, CURRENT_TIMESTAMP),

('LAB-SERVER-01', '192.168.1.101', '00:1A:2B:3C:4D:5F', 'Windows Server 2022',
'20348.2227', 'DataCenter', 'AMD Ryzen 9 5950X', 16, 32,
'x64', 64.0, 1024.0, 'HP', 'ProLiant DL380', 'SN987654321',
'ServerAdmin', 1, CURRENT_TIMESTAMP),

('WORKSTATION-02', '192.168.1.102', '00:1A:2B:3C:4D:60', 'Windows 10 Pro',
'19045.3803', 'Professional', 'Intel Core i5-11600', 6, 12,
'x64', 16.0, 256.0, 'Lenovo', 'ThinkCentre M70q', 'SN456789123',
'User1', 1, CURRENT_TIMESTAMP);
```

**Output:**

```
Query OK, 3 rows affected
```

**Verification Query:**

```sql
SELECT id, hostname, ip_address, os_info, cpu_name, total_memory_gb 
FROM systems;
```

**Output:**

```
+----+------------------+---------------+----------------------+-----------------------+-----------------+
| id | hostname         | ip_address    | os_info              | cpu_name              | total_memory_gb |
+----+------------------+---------------+----------------------+-----------------------+-----------------+
| 1  | DESKTOP-ABC123   | 192.168.1.100 | Windows 11 Pro       | Intel Core i7-12700K  | 32.0            |
| 2  | LAB-SERVER-01    | 192.168.1.101 | Windows Server 2022  | AMD Ryzen 9 5950X     | 64.0            |
| 3  | WORKSTATION-02   | 192.168.1.102 | Windows 10 Pro       | Intel Core i5-11600   | 16.0            |
+----+------------------+---------------+----------------------+-----------------------+-----------------+
```

---

## 3. Populate alerts Table

**Query:**

```sql
INSERT INTO alerts (system_id, alert_type, severity, message, is_resolved)
VALUES 
(1, 'CPU', 'WARNING', 'CPU usage exceeded 80% for 5 minutes', 0),
(1, 'MEMORY', 'CRITICAL', 'Memory usage at 95% - immediate action required', 0),
(2, 'DISK', 'WARNING', 'Disk usage at 85% on drive C:', 1),
(3, 'NETWORK', 'INFO', 'Network latency detected', 1);
```

**Output:**

```
Query OK, 4 rows affected
```

**Verification Query:**

```sql
SELECT id, system_id, alert_type, severity, message, is_resolved 
FROM alerts;
```

**Output:**

```
+----+-----------+------------+----------+-----------------------------------------------+-------------+
| id | system_id | alert_type | severity | message                                       | is_resolved |
+----+-----------+------------+----------+-----------------------------------------------+-------------+
| 1  | 1         | CPU        | WARNING  | CPU usage exceeded 80% for 5 minutes          | 0           |
| 2  | 1         | MEMORY     | CRITICAL | Memory usage at 95% - immediate action reqd   | 0           |
| 3  | 2         | DISK       | WARNING  | Disk usage at 85% on drive C:                 | 1           |
| 4  | 3         | NETWORK    | INFO     | Network latency detected                      | 1           |
+----+-----------+------------+----------+-----------------------------------------------+-------------+
```

---

## 4. Populate metrics Table

**Query:**

```sql
INSERT INTO metrics (system_id, cpu_usage, memory_percent, memory_used,
disk_free, disk_usage, disk_read_bytes, disk_write_bytes,
network_sent, network_recv, process_count, uptime_seconds, uptime_human)
VALUES 
(1, 45.2, 62.5, 20000000000, 230000000000, 55.0, 150000000000, 98000000000,
 45000000000, 32000000000, 156, 86400, '1 day, 0:00:00'),

(2, 28.7, 48.3, 30000000000, 512000000000, 50.0, 256000000000, 178000000000,
 120000000000, 89000000000, 203, 172800, '2 days, 0:00:00'),

(3, 65.8, 75.2, 12000000000, 128000000000, 50.0, 89000000000, 45000000000,
 23000000000, 18000000000, 98, 43200, '12 hours, 0:00:00');
```

**Output:**

```
Query OK, 3 rows affected
```

**Verification Query:**

```sql
SELECT id, system_id, cpu_usage, memory_percent, disk_usage, 
       process_count, uptime_human
FROM metrics;
```

**Output:**

```
+----+-----------+-----------+----------------+------------+---------------+------------------+
| id | system_id | cpu_usage | memory_percent | disk_usage | process_count | uptime_human     |
+----+-----------+-----------+----------------+------------+---------------+------------------+
| 1  | 1         | 45.2      | 62.5           | 55.0       | 156           | 1 day, 0:00:00   |
| 2  | 2         | 28.7      | 48.3           | 50.0       | 203           | 2 days, 0:00:00  |
| 3  | 3         | 65.8      | 75.2           | 50.0       | 98            | 12 hours, 0:00:00|
+----+-----------+-----------+----------------+------------+---------------+------------------+
```

---

## 5. Populate tickets Table

**Query:**

```sql
INSERT INTO tickets (system_id, message, status, resolved_at)
VALUES 
(1, 'System running slow - needs investigation', 'OPEN', NULL),
(2, 'Disk cleanup required on C: drive', 'RESOLVED', '2025-12-27 14:30:00'),
(3, 'Software update needed for antivirus', 'OPEN', NULL),
(1, 'Network adapter driver issue', 'RESOLVED', '2025-12-26 10:15:00');
```

**Output:**

```
Query OK, 4 rows affected
```

**Verification Query:**

```sql
SELECT id, system_id, message, status, created_at, resolved_at 
FROM tickets;
```

**Output:**

```
+----+-----------+--------------------------------------------+----------+---------------------+---------------------+
| id | system_id | message                                    | status   | created_at          | resolved_at         |
+----+-----------+--------------------------------------------+----------+---------------------+---------------------+
| 1  | 1         | System running slow - needs investigation  | OPEN     | 2025-12-28 13:25:00 | NULL                |
| 2  | 2         | Disk cleanup required on C: drive          | RESOLVED | 2025-12-28 13:25:00 | 2025-12-27 14:30:00 |
| 3  | 3         | Software update needed for antivirus       | OPEN     | 2025-12-28 13:25:00 | NULL                |
| 4  | 1         | Network adapter driver issue               | RESOLVED | 2025-12-28 13:25:00 | 2025-12-26 10:15:00 |
+----+-----------+--------------------------------------------+----------+---------------------+---------------------+
```

---

## 6. Populate alert_settings Table

**Query:**

```sql
INSERT INTO alert_settings (system_id, cpu_threshold, memory_threshold, disk_threshold)
VALUES 
(1, 85.0, 90.0, 85.0),
(2, 80.0, 85.0, 80.0),
(3, 90.0, 90.0, 90.0),
(NULL, 90.0, 90.0, 90.0);  -- Global default settings
```

**Output:**

```
Query OK, 4 rows affected
```

**Verification Query:**

```sql
SELECT id, system_id, cpu_threshold, memory_threshold, disk_threshold 
FROM alert_settings;
```

**Output:**

```
+----+-----------+---------------+------------------+----------------+
| id | system_id | cpu_threshold | memory_threshold | disk_threshold |
+----+-----------+---------------+------------------+----------------+
| 1  | 1         | 85.0          | 90.0             | 85.0           |
| 2  | 2         | 80.0          | 85.0             | 80.0           |
| 3  | 3         | 90.0          | 90.0             | 90.0           |
| 4  | NULL      | 90.0          | 90.0             | 90.0           |
+----+-----------+---------------+------------------+----------------+
```

---

## Complete Population Script

**To populate all tables at once:**

```sql
-- 1. Users
INSERT INTO users (email, hashed_password, is_active) VALUES
('admin@resourcemonitor.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8J9z1K2vY3mQ4pL5wZy', 1),
('nthy2355@gmail.com', '$2b$12$8kF2xN9pW1mH3jK5vL7qXeYzP4tR6sW8uV0mN2kJ3hL9gF5dC1aB', 1),
('admin1@gmail.com', '$2b$12$3mT4nU5vK6wL7xM8yN9zA0P1qR2sT3uV4wX5yZ6aC7bD8eF9gH0i', 1);

-- 2. Systems
INSERT INTO systems (hostname, ip_address, mac_address, os_info, os_build, windows_edition, 
cpu_name, cpu_cores, cpu_threads, architecture, total_memory_gb, total_disk_gb, manufacturer, 
model, serial_number, username, is_active, last_seen) VALUES 
('DESKTOP-ABC123', '192.168.1.100', '00:1A:2B:3C:4D:5E', 'Windows 11 Pro', '22621.3007', 'Professional', 
'Intel Core i7-12700K', 12, 20, 'x64', 32.0, 512.0, 'Dell', 'OptiPlex 7090', 'SN123456789', 'Admin', 1, CURRENT_TIMESTAMP),
('LAB-SERVER-01', '192.168.1.101', '00:1A:2B:3C:4D:5F', 'Windows Server 2022', '20348.2227', 'DataCenter', 
'AMD Ryzen 9 5950X', 16, 32, 'x64', 64.0, 1024.0, 'HP', 'ProLiant DL380', 'SN987654321', 'ServerAdmin', 1, CURRENT_TIMESTAMP),
('WORKSTATION-02', '192.168.1.102', '00:1A:2B:3C:4D:60', 'Windows 10 Pro', '19045.3803', 'Professional', 
'Intel Core i5-11600', 6, 12, 'x64', 16.0, 256.0, 'Lenovo', 'ThinkCentre M70q', 'SN456789123', 'User1', 1, CURRENT_TIMESTAMP);

-- 3. Alerts
INSERT INTO alerts (system_id, alert_type, severity, message, is_resolved) VALUES 
(1, 'CPU', 'WARNING', 'CPU usage exceeded 80% for 5 minutes', 0),
(1, 'MEMORY', 'CRITICAL', 'Memory usage at 95% - immediate action required', 0),
(2, 'DISK', 'WARNING', 'Disk usage at 85% on drive C:', 1),
(3, 'NETWORK', 'INFO', 'Network latency detected', 1);

-- 4. Metrics
INSERT INTO metrics (system_id, cpu_usage, memory_percent, memory_used, disk_free, disk_usage, 
disk_read_bytes, disk_write_bytes, network_sent, network_recv, process_count, uptime_seconds, uptime_human) VALUES 
(1, 45.2, 62.5, 20000000000, 230000000000, 55.0, 150000000000, 98000000000, 45000000000, 32000000000, 156, 86400, '1 day, 0:00:00'),
(2, 28.7, 48.3, 30000000000, 512000000000, 50.0, 256000000000, 178000000000, 120000000000, 89000000000, 203, 172800, '2 days, 0:00:00'),
(3, 65.8, 75.2, 12000000000, 128000000000, 50.0, 89000000000, 45000000000, 23000000000, 18000000000, 98, 43200, '12 hours, 0:00:00');

-- 5. Tickets
INSERT INTO tickets (system_id, message, status, resolved_at) VALUES 
(1, 'System running slow - needs investigation', 'OPEN', NULL),
(2, 'Disk cleanup required on C: drive', 'RESOLVED', '2025-12-27 14:30:00'),
(3, 'Software update needed for antivirus', 'OPEN', NULL),
(1, 'Network adapter driver issue', 'RESOLVED', '2025-12-26 10:15:00');

-- 6. Alert Settings
INSERT INTO alert_settings (system_id, cpu_threshold, memory_threshold, disk_threshold) VALUES 
(1, 85.0, 90.0, 85.0),
(2, 80.0, 85.0, 80.0),
(3, 90.0, 90.0, 90.0),
(NULL, 90.0, 90.0, 90.0);
```

---

## Verification Summary

```sql
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL
SELECT 'systems', COUNT(*) FROM systems
UNION ALL
SELECT 'alerts', COUNT(*) FROM alerts
UNION ALL
SELECT 'metrics', COUNT(*) FROM metrics
UNION ALL
SELECT 'tickets', COUNT(*) FROM tickets
UNION ALL
SELECT 'alert_settings', COUNT(*) FROM alert_settings;
```

**Output:**

```
+----------------+-----------+
| table_name     | row_count |
+----------------+-----------+
| users          | 3         |
| systems        | 3         |
| alerts         | 4         |
| metrics        | 3         |
| tickets        | 4         |
| alert_settings | 4         |
+----------------+-----------+
```
