import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getSystem, getMetrics, deleteSystem, getTickets, updateTicketStatus, exportMetrics } from '../services/api';
import { Line, Doughnut } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
    ArcElement,
} from 'chart.js';
import { ArrowLeft, Cpu, HardDrive, Wifi, Activity, Server, Clock, Layers, ArrowUp, ArrowDown, Network, Globe, Box, User, Tag, Battery } from 'lucide-react';
import ProcessList from '../components/ProcessList';
import DriverListModal from '../components/DriverListModal';
import AlertConfigModal from '../components/AlertConfigModal';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
    ArcElement
);

const THEME = {
    cpu: '#F97316',    // Orange-500
    memory: '#10B981', // Emerald-500
    disk: '#FACC15',   // Yellow-400
    netUp: '#3B82F6',  // Blue-500
    netDown: '#6366F1',// Indigo-500
    diskRead: '#06b6d4', // Cyan-500
    diskWrite: '#ec4899' // Pink-500
};

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
    },
    scales: {
        x: {
            grid: { color: 'rgba(255,255,255,0.03)' },
            ticks: { color: '#666', font: { family: 'JetBrains Mono', size: 10 } },
        },
        y: {
            grid: { color: 'rgba(255,255,255,0.03)' },
            ticks: { color: '#666', font: { family: 'JetBrains Mono', size: 10 } },
        },
    },
    elements: {
        point: { radius: 0 },
        line: { borderWidth: 2 },
    },
};



const SystemDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [system, setSystem] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [processingTicket, setProcessingTicket] = useState(null);
    const [showDriverList, setShowDriverList] = useState(false);
    const [showAlertConfig, setShowAlertConfig] = useState(false);

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 1000);
        return () => clearInterval(interval);
    }, [id]);

    const fetchData = async () => {
        try {
            // Fetch System Details first (CRITICAL)
            try {
                const systemData = await getSystem(id);
                setSystem(systemData);
            } catch (err) {
                console.error("Failed to fetch system info:", err);
                // If system info fails, we can't show much, so let it bubble or handle critical failure
                throw err;
            }

            // Fetch Metrics (Non-critical)
            try {
                const metricsData = await getMetrics(id, 100);
                if (Array.isArray(metricsData)) {
                    setMetrics(metricsData.reverse());
                }
            } catch (err) {
                console.warn("Failed to fetch metrics (non-critical):", err);
            }

            // Fetch Tickets (Non-critical)
            try {
                const ticketsData = await getTickets(id);
                setTickets(ticketsData);
            } catch (err) {
                console.warn("Failed to fetch tickets (non-critical):", err);
            }

            setLoading(false);
        } catch (error) {
            console.error("Critical Error fetching system:", error);
            setLoading(false);
        }
    };

    const handleDelete = async () => {
        if (window.confirm(`Are you sure you want to delete ${system.hostname}? This action cannot be undone.`)) {
            try {
                await deleteSystem(id);
                navigate('/');
            } catch (error) {
                console.error("Failed to delete system:", error);
                alert("Failed to delete system.");
            }
        }
    };

    const handleUpdateStatus = async (ticketId, newStatus) => {
        try {
            setProcessingTicket(ticketId);
            await updateTicketStatus(ticketId, newStatus);
            // Refresh tickets
            const updatedTickets = await getTickets(id);
            setTickets(updatedTickets);
        } catch (error) {
            console.error("Failed to update status:", error);
            alert("Failed to update status.");
        } finally {
            setProcessingTicket(null);
        }
    };

    const handleExport = async () => {
        try {
            const response = await exportMetrics(id);
            // Create a blob link to download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;

            // Extract filename from header or default
            let filename = `metrics_${system.hostname}.csv`;
            const contentDisposition = response.headers['content-disposition'];
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename=(.+)/);
                if (filenameMatch.length === 2) filename = filenameMatch[1];
            }

            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error("Failed to export CSV:", error);
            alert("Failed to export metrics.");
        }
    };

    if (loading) return <div className="loading">Loading System Data...</div>;
    if (!system) return <div className="error-state" style={{ padding: '40px', textAlign: 'center', color: '#ff4444' }}>
        <h2>System Not Found</h2>
        <p>Could not load system details. The system might have been deleted or the server is unreachable.</p>
        <Link to="/" style={{ color: '#fff', textDecoration: 'underline' }}>Return to Dashboard</Link>
    </div>;

    const timestamps = metrics.map(m => {
        // Fix for SQLite losing timezone info: Treat naive strings as UTC
        const isoString = m.timestamp.includes('Z') || m.timestamp.includes('+')
            ? m.timestamp
            : m.timestamp + 'Z';
        const d = new Date(isoString);
        return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    });

    const latestMetric = metrics.length > 0 ? metrics[metrics.length - 1] : null;

    // Calculate real-time network and disk speed
    let networkUp = 0;
    let networkDown = 0;
    let diskRead = 0;
    let diskWrite = 0;

    if (metrics.length >= 2) {
        const current = metrics[metrics.length - 1];
        const prev = metrics[metrics.length - 2];
        const timeDiff = (new Date(current.timestamp) - new Date(prev.timestamp)) / 1000;

        if (timeDiff > 0) {
            networkUp = ((current.network_sent - prev.network_sent) / timeDiff / 1024).toFixed(1);
            networkDown = ((current.network_recv - prev.network_recv) / timeDiff / 1024).toFixed(1);

            // Disk I/O (MB/s)
            diskRead = ((current.disk_read_bytes || 0) - (prev.disk_read_bytes || 0)) / timeDiff / 1024 / 1024;
            diskWrite = ((current.disk_write_bytes || 0) - (prev.disk_write_bytes || 0)) / timeDiff / 1024 / 1024;

            // Handle restart case or first run
            if (networkUp < 0) networkUp = 0;
            if (networkDown < 0) networkDown = 0;
            if (diskRead < 0) diskRead = 0;
            if (diskWrite < 0) diskWrite = 0;
        }
    }

    const createChartData = (label, data, color) => ({
        labels: timestamps,
        datasets: [{
            label,
            data,
            borderColor: color,
            backgroundColor: `${color}15`,
            tension: 0.1,
            fill: true,
        }]
    });

    const cpuData = createChartData('CPU %', metrics.map(m => m.cpu_usage), THEME.cpu);
    const memoryData = createChartData('Memory GB', metrics.map(m => (m.memory_used / 1024 / 1024 / 1024).toFixed(2)), THEME.memory);
    const diskData = createChartData('Disk %', metrics.map(m => m.disk_usage), THEME.disk);

    const calculateRate = (metricKey) => {
        return metrics.map((m, i) => {
            if (i === 0) return 0;
            const prev = metrics[i - 1];
            const timeDiff = (new Date(m.timestamp) - new Date(prev.timestamp)) / 1000;
            if (timeDiff <= 0) return 0;
            const bytesDiff = m[metricKey] - prev[metricKey];
            if (bytesDiff < 0) return 0; // Handle restart/reset
            return (bytesDiff / timeDiff / 1024).toFixed(1); // KB/s
        });
    };

    const networkData = {
        labels: timestamps,
        datasets: [
            {
                label: 'Upload KB/s',
                data: calculateRate('network_sent'),
                borderColor: THEME.netUp,
                backgroundColor: `${THEME.netUp}15`,
                tension: 0.3,
                fill: true,
            },
            {
                label: 'Download KB/s',
                data: calculateRate('network_recv'),
                borderColor: THEME.netDown,
                backgroundColor: `${THEME.netDown}15`,
                tension: 0.3,
                fill: true,
            }
        ]
    };

    const diskIoData = {
        labels: timestamps,
        datasets: [
            {
                label: 'Read MB/s',
                data: calculateRate('disk_read_bytes').map(v => (v / 1024).toFixed(1)), // KB/s -> MB/s
                borderColor: THEME.diskRead,
                backgroundColor: `${THEME.diskRead}15`,
                tension: 0.3,
                fill: true,
            },
            {
                label: 'Write MB/s',
                data: calculateRate('disk_write_bytes').map(v => (v / 1024).toFixed(1)), // KB/s -> MB/s
                borderColor: THEME.diskWrite,
                backgroundColor: `${THEME.diskWrite}15`,
                tension: 0.3,
                fill: true,
            }
        ]
    };

    const formatUptime = (bootTime) => {
        if (!bootTime) return 'N/A';
        const boot = new Date(bootTime);
        const now = new Date();
        const diff = now - boot;
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const days = Math.floor(hours / 24);
        const remainingHours = hours % 24;
        if (days > 0) return `${days}d ${remainingHours}h`;
        return `${hours}h`;
    };

    const renderSpecItem = (label, value, Icon, valueColor = null) => {
        if (!value) return null;
        return (
            <div className="info-card" title={label}>
                {Icon && <Icon size={20} className="icon-wrapper" />}
                <div className="content">
                    <span className="label">{label}</span>
                    <span className="value" style={valueColor ? { color: valueColor } : {}}>{value}</span>
                </div>
            </div>
        );
    };

    return (
        <div className="system-detail container">
            <div className="detail-header">
                <Link to="/" className="back-link">
                    <ArrowLeft size={16} /> Back to Dashboard
                </Link>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', marginTop: '8px' }}>
                    <h1 style={{ margin: 0 }}>{system.user_label || system.hostname}</h1>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <button onClick={() => setShowDriverList(true)} style={{ backgroundColor: '#111', color: '#fff', border: '1px solid #444', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontFamily: 'inherit', fontWeight: 'bold' }}>
                            📦 DRIVERS
                        </button>
                        <button onClick={() => setShowAlertConfig(true)} style={{ backgroundColor: '#111', color: '#ff6600', border: '1px solid #ff6600', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontFamily: 'inherit', fontWeight: 'bold' }}>
                            ⚠ CONFIG ALERTS
                        </button>
                        <button onClick={handleExport} style={{ backgroundColor: '#111', color: '#ffcc00', border: '1px solid #ffcc00', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontFamily: 'inherit', fontWeight: 'bold' }}>
                            EXPORT CSV
                        </button>
                        <button onClick={handleDelete} className="delete-btn" style={{ backgroundColor: '#330000', color: '#ff4444', border: '1px solid #ff4444', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontFamily: 'inherit', fontWeight: 'bold' }}>
                            DELETE SYSTEM
                        </button>
                    </div>
                </div>
                <p className="subtitle" style={{ margin: '8px 0 0 0', fontSize: '0.85rem', color: '#aaa' }}>
                    {system.os_info} •
                    <span className={`status-badge ${system.is_active ? 'online' : 'offline'}`} style={{ marginLeft: '0.5rem' }}>
                        {system.is_active ? '● Online' : '○ Offline'}
                    </span>
                    {latestMetric && (
                        <span className="last-updated" style={{ marginLeft: '0.5rem' }}>
                            • Last Updated: {new Date(latestMetric.timestamp.includes('Z') || latestMetric.timestamp.includes('+') ? latestMetric.timestamp : latestMetric.timestamp + 'Z').toLocaleTimeString()}
                        </span>
                    )}
                </p>
            </div>

            {/* System Info Grid */}
            <div className="info-grid">
                <div className="info-card" title="Central Processing Unit model and specifications">
                    <Cpu size={20} className="icon-wrapper" />
                    <div className="content">
                        <span className="label">Processor</span>
                        <span className="value">{system.cpu_name || 'Unknown'}</span>
                    </div>
                </div>
                <div className="info-card" title="Physical cores / Logical threads (with hyperthreading)">
                    <Layers size={20} className="icon-wrapper" />
                    <div className="content">
                        <span className="label">Cores / Threads</span>
                        <span className="value">{system.cpu_cores || '?'} / {system.cpu_threads || '?'}</span>
                    </div>
                </div>
                <div className="info-card" title="Operating system name and version">
                    <Server size={20} className="icon-wrapper" />
                    <div className="content">
                        <span className="label">Operating System</span>
                        <span className="value">{system.windows_edition || system.os_info}</span>
                    </div>
                </div>
                <div className="info-card" title="Primary IP Address">
                    <Wifi size={20} className="icon-wrapper" />
                    <div className="content">
                        <span className="label">IP Address</span>
                        <span className="value">{system.ip_address}</span>
                    </div>
                </div>
            </div>

            {/* Categorized System Specs */}
            <div className="specs-container">

                {/* Device Info */}
                <div className="spec-group">
                    <h3>Device Info</h3>
                    <div className="specs-grid-group">
                        {renderSpecItem('Manufacturer', system.manufacturer)}
                        {renderSpecItem('Model', system.model)}
                        {renderSpecItem('Serial Number', system.serial_number)}
                        {renderSpecItem('BIOS Version', system.bios_version)}
                        {renderSpecItem('Architecture', system.architecture)}
                    </div>
                </div>

                {/* Resources */}
                <div className="spec-group">
                    <h3>Resources</h3>
                    <div className="specs-grid-group">
                        {renderSpecItem('GPU', system.gpu_name)}
                        {renderSpecItem('Disk Model', system.disk_model)}
                        {renderSpecItem('Total RAM', system.total_memory_gb ? `${system.total_memory_gb} GB` : null)}

                        {system.battery_percent !== null && (
                            <div className="spec-item" style={{ background: '#111', padding: '12px' }}>
                                <span style={{ fontSize: '10px', color: '#666', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Battery</span>
                                <div style={{ marginTop: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    <div style={{ flex: 1, height: '6px', background: '#333', borderRadius: '3px', overflow: 'hidden' }}>
                                        <div style={{
                                            width: `${system.battery_percent}%`,
                                            height: '100%',
                                            background: system.battery_percent > 50 ? '#00ff66' : system.battery_percent > 20 ? '#ffcc00' : '#ff3333',
                                            borderRadius: '3px'
                                        }}></div>
                                    </div>
                                    <span style={{ fontSize: '11px', color: '#fff' }}>
                                        {system.battery_percent}% {system.is_plugged_in && '⚡'}
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Network */}
                <div className="spec-group">
                    <h3>Network</h3>
                    <div className="info-grid">
                        {renderSpecItem('Adapter', system.network_adapter, Network)}
                        {renderSpecItem('MAC Address', system.mac_address, Tag)}
                        {renderSpecItem('Public IP', 'N/A', Globe)}
                    </div>
                </div>

                {/* Environment */}
                <div className="spec-group">
                    <h3>Environment</h3>
                    <div className="info-grid">
                        {renderSpecItem('OS Build', system.os_build, Box)}
                        {renderSpecItem('User', system.domain ? `${system.domain}\\${system.username}` : system.username, User)}
                        {renderSpecItem('Timezone', system.timezone, Clock)}
                        {renderSpecItem('Agent Version', system.agent_version ? `v${system.agent_version}` : null, Tag)}
                    </div>
                </div>
            </div>

            {/* Live Stats */}
            {latestMetric && (
                <div className="live-stats">
                    <div className="live-stat" title="Current CPU utilization across all cores">
                        <div className="stat-label">CPU</div>
                        <div className="stat-value">{latestMetric.cpu_usage}<span className="stat-unit">%</span></div>
                    </div>

                    <div className="live-stat" title="Number of running processes on this system">
                        <div className="stat-label">Processes</div>
                        <div className="stat-value">{latestMetric.process_count || 0}</div>
                    </div>
                    <div className="live-stat" title="Amount of physical RAM currently in use">
                        <div className="stat-label">RAM Used</div>
                        <div className="stat-value">{(latestMetric.memory_used / 1024 / 1024 / 1024).toFixed(1)}<span className="stat-unit">GB</span></div>
                    </div>
                    <div className="live-stat" title="Time since last system restart">
                        <div className="stat-label">Uptime</div>
                        <div className="stat-value">{latestMetric.uptime_human || formatUptime(latestMetric.boot_time)}</div>
                    </div>

                    <div className="live-stat" title="Current network upload speed">
                        <div className="stat-label">Net Upload</div>
                        <div className="stat-value" style={{ color: THEME.netUp }}>
                            <ArrowUp size={12} style={{ display: 'inline', marginRight: '4px' }} />
                            {networkUp}<span className="stat-unit">KB/s</span>
                        </div>
                    </div>
                    <div className="live-stat" title="Current network download speed">
                        <div className="stat-label">Net Download</div>
                        <div className="stat-value" style={{ color: THEME.netDown }}>
                            <ArrowDown size={12} style={{ display: 'inline', marginRight: '4px' }} />
                            {networkDown}<span className="stat-unit">KB/s</span>
                        </div>
                    </div>
                </div>
            )}

            {/* Charts - Full Width Vertical Layout */}
            <div className="charts-grid" style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
                <div className="chart-card" style={{ height: '300px' }}>
                    <h3>CPU Usage</h3>
                    <Line options={chartOptions} data={cpuData} />
                </div>
                <div className="chart-card" style={{ height: '300px' }}>
                    <h3>Memory Usage</h3>
                    <Line options={chartOptions} data={memoryData} />
                </div>

                <div className="chart-card" style={{ height: '300px' }}>
                    <h3>Network I/O</h3>
                    <Line options={{ ...chartOptions, plugins: { legend: { display: true, labels: { color: '#666', font: { family: 'JetBrains Mono', size: 10 } } } } }} data={networkData} />
                </div>
            </div>

            {/* Top Processes */}
            {latestMetric && latestMetric.top_processes && (
                <ProcessList processes={latestMetric.top_processes} />
            )}

            {/* Support Tickets */}
            <div className="process-list-container" style={{ marginTop: '32px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '14px', marginBottom: '20px', color: '#fff', textTransform: 'uppercase', letterSpacing: '0.15em' }}>
                    <span style={{ color: '#ff6600' }}>🎫</span> Support Tickets
                </h3>
                {tickets.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '30px', color: '#aaa', fontStyle: 'italic', fontSize: '13px' }}>
                        No support tickets found for this system.
                    </div>
                ) : (
                    <div className="table-responsive">
                        <table className="process-table">
                            <thead>
                                <tr>
                                    <th>Status</th>
                                    <th>Issue</th>
                                    <th>Reported</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {tickets.map(ticket => (
                                    <tr key={ticket.id} style={{ borderBottom: '1px solid #222' }}>
                                        <td style={{ padding: '12px' }}>
                                            <span style={{
                                                fontSize: '10px',
                                                padding: '4px 8px',
                                                borderRadius: '4px',
                                                background: ticket.status === 'RESOLVED' ? 'rgba(0, 255, 102, 0.15)' :
                                                    ticket.status === 'IN_PROGRESS' ? 'rgba(255, 204, 0, 0.15)' : 'rgba(255, 68, 68, 0.15)',
                                                color: ticket.status === 'RESOLVED' ? '#00ff66' :
                                                    ticket.status === 'IN_PROGRESS' ? '#ffcc00' : '#ff4444',
                                                border: `1px solid ${ticket.status === 'RESOLVED' ? '#00ff66' :
                                                    ticket.status === 'IN_PROGRESS' ? '#ffcc00' : '#ff4444'}`,
                                                fontWeight: 'bold',
                                                letterSpacing: '0.05em'
                                            }}>
                                                {ticket.status}
                                            </span>
                                        </td>
                                        <td style={{ color: '#fff', fontSize: '13px', whiteSpace: 'pre-wrap', padding: '12px' }}>{ticket.message}</td>
                                        <td style={{ color: '#aaa', fontSize: '12px', padding: '12px' }}>
                                            {new Date(ticket.created_at).toLocaleString()}
                                            {ticket.resolved_at && <div style={{ fontSize: '10px', color: '#00ff66' }}>Resolved: {new Date(ticket.resolved_at).toLocaleString()}</div>}
                                        </td>
                                        <td style={{ padding: '12px' }}>
                                            {ticket.status === 'OPEN' && (
                                                <button
                                                    onClick={() => handleUpdateStatus(ticket.id, 'IN_PROGRESS')}
                                                    disabled={processingTicket === ticket.id}
                                                    style={{
                                                        background: processingTicket === ticket.id ? '#333' : '#111',
                                                        border: '1px solid #ffcc00',
                                                        color: '#ffcc00',
                                                        padding: '6px 12px',
                                                        cursor: processingTicket === ticket.id ? 'not-allowed' : 'pointer',
                                                        fontSize: '11px',
                                                        borderRadius: '4px',
                                                        textTransform: 'uppercase',
                                                        fontWeight: 'bold'
                                                    }}
                                                >
                                                    {processingTicket === ticket.id ? 'Updating...' : '🛠 WORK ON'}
                                                </button>
                                            )}

                                            {ticket.status === 'IN_PROGRESS' && (
                                                <button
                                                    onClick={() => handleUpdateStatus(ticket.id, 'RESOLVED')}
                                                    disabled={processingTicket === ticket.id}
                                                    style={{
                                                        background: processingTicket === ticket.id ? '#333' : '#111',
                                                        border: '1px solid #00ff66',
                                                        color: '#00ff66',
                                                        padding: '6px 12px',
                                                        cursor: processingTicket === ticket.id ? 'not-allowed' : 'pointer',
                                                        fontSize: '11px',
                                                        borderRadius: '4px',
                                                        textTransform: 'uppercase',
                                                        fontWeight: 'bold'
                                                    }}
                                                >
                                                    {processingTicket === ticket.id ? 'Resolving...' : '✅ RESOLVE'}
                                                </button>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Components */}
            <AlertConfigModal
                isOpen={showAlertConfig}
                onClose={() => setShowAlertConfig(false)}
                systemId={parseInt(id)}
            />
            <DriverListModal
                isOpen={showDriverList}
                onClose={() => setShowDriverList(false)}
                drivers={system.drivers || []}
            />
        </div>
    );
};

export default SystemDetail;
