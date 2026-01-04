import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getSystems, getAlerts } from '../services/api';
import { Activity, AlertTriangle, Clock, Cpu, HardDrive, MemoryStick, Copy, Check, Settings } from 'lucide-react';
import LoadingSkeleton from '../components/LoadingSkeleton';
import AlertConfigModal from '../components/AlertConfigModal';

const Dashboard = () => {
    const [systems, setSystems] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [copied, setCopied] = useState(false);
    const [isConfigOpen, setIsConfigOpen] = useState(false);

    // Get server URL from current page location
    const serverUrl = `${window.location.protocol}//${window.location.hostname}:8000`;

    useEffect(() => {
        let isMounted = true;
        const poll = async () => {
            if (!isMounted) return;
            await fetchData();
            if (isMounted) setTimeout(poll, 3000); // 3-second interval, waits for previous fetch
        };
        poll();
        return () => { isMounted = false; };
    }, []);

    const fetchData = async () => {
        try {
            const [systemsData, alertsData] = await Promise.all([
                getSystems(),
                getAlerts(false)
            ]);
            setSystems(systemsData);
            setAlerts(alertsData);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching data:", error);
            setLoading(false);
        }
    };

    const copyServerUrl = () => {
        navigator.clipboard.writeText(serverUrl);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (loading && systems.length === 0) return <LoadingSkeleton count={4} />;

    const formatDate = (dateStr) => {
        if (!dateStr) return 'Never';
        const date = new Date(dateStr);
        return date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="dashboard container">
            <header className="page-header">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
                    <div>
                        <h1>System Overview</h1>
                        <p className="subtitle">Real-time resource monitoring</p>
                    </div>
                    <div className="server-url-box" title="Share this URL with agents to connect">
                        <span className="server-url-label">SERVER URL</span>
                        <div className="server-url-value">
                            <code>{serverUrl}</code>
                            <button onClick={copyServerUrl} className="copy-btn" title={copied ? "Copied!" : "Copy to clipboard"}>
                                {copied ? <Check size={14} /> : <Copy size={14} />}
                            </button>
                        </div>
                    </div>
                </div>

                <div className="stats-summary">
                    <div className="stat-card" title="Total number of registered systems">
                        <span className="label">Total Systems</span>
                        <span className="value">{systems.length}</span>
                    </div>
                    <div className="stat-card" title="Systems currently sending metrics (active in last 5 seconds)">
                        <span className="label">Online</span>
                        <span className="value">{systems.filter(s => s.is_active).length}</span>
                    </div>
                    <div className="stat-card" title="Systems not responding (inactive for more than 5 seconds)">
                        <span className="label">Offline</span>
                        <span className="value">{systems.filter(s => !s.is_active).length}</span>
                    </div>
                    <div className={`stat-card ${alerts.length > 0 ? 'danger' : ''}`} title="Unresolved alerts requiring attention">
                        <span className="label">Active Alerts</span>
                        <span className="value">{alerts.length}</span>
                    </div>
                </div>
            </header>

            {alerts.length > 0 && (
                <section className="alerts-section">
                    <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                        <h2 style={{ margin: 0 }}>Active Alerts</h2>
                        <button
                            onClick={() => setIsConfigOpen(true)}
                            style={{
                                display: 'flex', alignItems: 'center', gap: '6px',
                                background: 'transparent', border: '1px solid #333',
                                color: '#aaa', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '12px'
                            }}
                            title="Configure Alert Thresholds"
                        >
                            <Settings size={14} /> Configure
                        </button>
                    </div>
                    <div className="alerts-list">
                        {alerts.slice(0, 5).map(alert => (
                            <div key={alert.id} className={`alert-item ${alert.severity.toLowerCase()}`}>
                                <AlertTriangle size={18} />
                                <div className="alert-content">
                                    <strong>{alert.alert_type} — System #{alert.system_id}</strong>
                                    <p>{alert.message}</p>
                                </div>
                                <span className="alert-time">{formatDate(alert.created_at)}</span>
                            </div>
                        ))}
                    </div>
                </section>
            )}

            <section className="systems-grid">
                {systems.map(system => (
                    <Link to={`/system/${system.id}`} key={system.id} className="system-card">
                        <div className="card-header">
                            <div className={`status-indicator ${system.is_active ? 'online' : 'offline'}`}></div>
                            <h3>{system.user_label || system.hostname}</h3>
                        </div>
                        <div className="card-body">
                            <p><strong>OS:</strong> {system.os_info}</p>
                            <p><strong>IP:</strong> {system.ip_address || 'N/A'}</p>

                            {(system.cpu_name || system.cpu_cores) && (
                                <div className="system-specs">
                                    {system.cpu_name && (
                                        <div className="spec-item" title="Central Processing Unit model">
                                            <span className="spec-label">Processor</span>
                                            <span className="spec-value">{system.cpu_name}</span>
                                        </div>
                                    )}
                                    {system.cpu_cores && (
                                        <div className="spec-item" title="Physical cores / Logical threads">
                                            <span className="spec-label">Cores / Threads</span>
                                            <span className="spec-value">{system.cpu_cores} / {system.cpu_threads}</span>
                                        </div>
                                    )}
                                    {system.total_memory_gb && (
                                        <div className="spec-item" title="Total physical RAM installed">
                                            <span className="spec-label">Total RAM</span>
                                            <span className="spec-value">{system.total_memory_gb} GB</span>
                                        </div>
                                    )}
                                    {system.architecture && (
                                        <div className="spec-item" title="CPU architecture (x64, ARM64, etc.)">
                                            <span className="spec-label">Architecture</span>
                                            <span className="spec-value">{system.architecture}</span>
                                        </div>
                                    )}
                                </div>
                            )}

                            <div className="last-seen">
                                <Clock size={14} />
                                <span>Last seen: {formatDate(system.last_seen)}</span>
                            </div>
                        </div>
                    </Link>
                ))}
            </section>

            <AlertConfigModal isOpen={isConfigOpen} onClose={() => setIsConfigOpen(false)} />
        </div>
    );
};

export default Dashboard;
