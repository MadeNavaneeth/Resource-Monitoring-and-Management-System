# System Architecture

## Overview
The Resource Monitoring System is a 3-tier application:

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│     AGENTS      │─────▶│     BACKEND     │◀─────│   DASHBOARD     │
│  (Lab PCs)      │ HTTP │  (FastAPI)      │ HTTP │   (React)       │
│  python+tkinter │      │  SQLite + WAL   │      │   Vite+Chart.js │
└─────────────────┘      └─────────────────┘      └─────────────────┘
        │                        │
        │  UDP (Auto-Discovery)  │
        └────────────────────────┘
```

## Data Flow

1.  **Agent** collects metrics (CPU, RAM, Disk, Network) every 1 second.
2.  **Agent** sends data via HTTP POST to `/api/v1/metrics`.
3.  **Backend** stores metrics in SQLite (WAL mode for high throughput).
4.  **Dashboard** polls `/api/v1/metrics` every 1 second and updates charts.

## Auto-Discovery (Zero-Config)

1.  **Backend** starts a `ServiceBeacon` thread that broadcasts its URL via UDP (port 54321).
2.  **Agent** listens on UDP port 54321 for 10 seconds on startup.
3.  On receiving the beacon, the Agent populates the "Server URL" field automatically.

## Security

| Mechanism     | Purpose                               |
|---------------|---------------------------------------|
| **API Key**   | Authenticates Agents (header: `X-API-Key`) |
| **JWT**       | Authenticates Dashboard Users          |

Default keys are provided for "Zero-Config" lab use. For production, set `AGENT_API_KEY` and `JWT_SECRET_KEY` environment variables.

## Database

- **Engine**: SQLite with WAL (Write-Ahead Logging) enabled.
- **Retention**: Metrics older than 24 hours are automatically deleted by a background `MetricCleaner` task.

## Key Files

| File                          | Purpose                                  |
|-------------------------------|------------------------------------------|
| `backend/app/main.py`         | FastAPI entry point, starts beacon/cleanup |
| `backend/app/core/discovery.py` | UDP Beacon for auto-discovery           |
| `backend/app/core/cleanup.py` | Background task for data retention       |
| `agent/gui.py`                | Tkinter GUI for the agent                |
| `agent/discovery.py`          | UDP listener for finding the server      |
| `dashboard/src/pages/*`       | React pages for Dashboard/SystemDetail   |
