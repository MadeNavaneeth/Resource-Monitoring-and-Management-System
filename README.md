# Resource Monitoring and Management System

A high-performance, **Zero-Configuration** monitoring solution for labs and classrooms. Track CPU, Memory, Disk, and Network I/O from multiple computers in real-time.

## ✨ Key Features

- **🚀 Zero-Config Deployment**: Agents auto-discover the server via UDP broadcast. No IP typing required.
- **⚡ 1-Second Updates**: Real-time, laser-accurate monitoring.
- **🎨 Modern UI**: Industrial "Teenage Engineering" design aesthetic.
- **📊 Automatic Alerting**: Detects high CPU, Memory, and Disk usage.
- **🧹 Self-Cleaning**: Automatically deletes data older than 24 hours.

---

## 🚀 Quick Start (Server/Admin)

**Prerequisites:** Python 3.9+, Node.js 18+

**1-Click Run:**
```bash
# Double-click or run from terminal:
run_all.bat
```
This starts:
1.  **Backend API** → `http://localhost:8000`
2.  **Dashboard** → `http://localhost:5173`
3.  **Local Agent** (for testing)

---

## 💻 Lab Deployment (Client PCs)

1.  **Build the Agent** (on Admin PC): Run `agent/build_exe.bat`.
2.  **Copy `agent/dist/SysMonitorAgent.exe`** to a USB drive.
3.  **Run on Lab PCs**: Double-click the `.exe`. It will:
    - Automatically find the server.
    - Automatically name itself using the PC's hostname.
4.  Click **START**. Done.

---

## 🛠️ Technology Stack

| Component   | Technology                      |
|-------------|---------------------------------|
| **Backend** | Python (FastAPI) + SQLite (WAL) |
| **Frontend**| React + Vite + Chart.js         |
| **Agent**   | Python (Psutil + Tkinter)       |

---

## 🔑 Security

- **Default Mode**: Uses a shared `secret-agent-key` for lab convenience.
- **Production Mode**: Set `AGENT_API_KEY` and `JWT_SECRET_KEY` environment variables before deploying.

---

## 📄 License

MIT