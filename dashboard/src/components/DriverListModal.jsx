import React, { useState, useMemo } from 'react';
import { X, Search, Package, ChevronRight, ChevronDown } from 'lucide-react';

const DriverListModal = ({ isOpen, onClose, drivers = [] }) => {
    const [search, setSearch] = useState('');
    const [expandedGroups, setExpandedGroups] = useState({});

    // Toggle group expansion
    const toggleGroup = (group) => {
        setExpandedGroups(prev => ({
            ...prev,
            [group]: !prev[group]
        }));
    };

    // Filter and Group Drivers
    const groupedDrivers = useMemo(() => {
        const groups = {};

        // Default expansion state for all groups initially
        const initialExpanded = {};

        drivers.forEach(d => {
            // Filter match
            const matchesSearch = !search ||
                (d.DeviceName && d.DeviceName.toLowerCase().includes(search.toLowerCase())) ||
                (d.DeviceClass && d.DeviceClass.toLowerCase().includes(search.toLowerCase()));

            if (matchesSearch) {
                const groupName = d.DeviceClass || 'Uncategorized';
                if (!groups[groupName]) {
                    groups[groupName] = [];
                    // Auto-expand all if searching, otherwise collapse by default (or expand, user preference)
                    // Let's expand all by default for better visibility
                    initialExpanded[groupName] = true;
                }
                groups[groupName].push(d);
            }
        });

        // If user hasn't interacted, use initial state. 
        // But we need to sync this state. simpler approach: 
        // If search is active, force expand all.

        return Object.entries(groups).sort((a, b) => a[0].localeCompare(b[0]));
    }, [drivers, search]);

    // Handle initial expansion on search change
    React.useEffect(() => {
        if (search) {
            setExpandedGroups(prev => {
                const all = {};
                groupedDrivers.forEach(([group]) => { all[group] = true; });
                return all;
            });
        }
    }, [search]); // Only re-run when search string changes

    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            backdropFilter: 'blur(5px)'
        }}>
            <div style={{
                background: '#111',
                border: '1px solid #333',
                borderRadius: '8px',
                width: '800px',
                maxWidth: '90%',
                maxHeight: '80vh',
                display: 'flex',
                flexDirection: 'column',
                boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)'
            }}>
                {/* Header */}
                <div style={{
                    padding: '20px',
                    borderBottom: '1px solid #222',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                }}>
                    <h2 style={{
                        margin: 0,
                        fontSize: '16px',
                        color: '#fff',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                    }}>
                        <Package size={20} color="#666" />
                        Installed Drivers
                        <span style={{
                            fontSize: '11px',
                            background: '#222',
                            padding: '2px 8px',
                            borderRadius: '12px',
                            color: '#888'
                        }}>
                            {drivers.length}
                        </span>
                    </h2>
                    <button
                        onClick={onClose}
                        style={{ background: 'none', border: 'none', color: '#666', cursor: 'pointer' }}
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Search */}
                <div style={{ padding: '16px 20px', borderBottom: '1px solid #222' }}>
                    <div style={{ position: 'relative' }}>
                        <Search size={16} color="#444" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
                        <input
                            type="text"
                            placeholder="Search devices..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            style={{
                                width: '100%',
                                background: '#0a0a0a',
                                border: '1px solid #333',
                                padding: '10px 10px 10px 36px',
                                color: '#fff',
                                borderRadius: '4px',
                                fontSize: '13px',
                                fontFamily: 'monospace'
                            }}
                        />
                    </div>
                </div>

                {/* List */}
                <div style={{
                    flex: 1,
                    overflowY: 'auto',
                    padding: '0'
                }}>
                    {groupedDrivers.map(([group, filteredDrivers]) => {
                        // Default to true if key doesn't exist yet (first render logic handled mostly by effect, but as fallback)
                        const isExpanded = expandedGroups[group] !== undefined ? expandedGroups[group] : true; // Default expanded

                        return (
                            <div key={group} style={{ borderBottom: '1px solid #222' }}>
                                <div
                                    onClick={() => toggleGroup(group)}
                                    style={{
                                        padding: '12px 20px',
                                        background: '#161616',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '10px',
                                        userSelect: 'none'
                                    }}
                                >
                                    {isExpanded ? <ChevronDown size={14} color="#888" /> : <ChevronRight size={14} color="#888" />}
                                    <span style={{ color: '#ddd', fontSize: '13px', fontWeight: 'bold' }}>{group}</span>
                                    <span style={{ fontSize: '11px', color: '#555', marginLeft: 'auto' }}>{filteredDrivers.length} devices</span>
                                </div>

                                {isExpanded && (
                                    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
                                        <tbody>
                                            {filteredDrivers.map((driver, i) => (
                                                <tr key={i} style={{ borderBottom: '1px solid #1a1a1a' }}>
                                                    <td style={{ padding: '8px 20px 8px 44px', color: '#bbb' }}>{driver.DeviceName}</td>
                                                    <td style={{ padding: '8px', color: '#666', fontFamily: 'monospace', width: '100px' }}>{driver.DriverVersion}</td>
                                                    <td style={{ padding: '8px', color: '#555', width: '100px' }}>{driver.DriverDate}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                )}
                            </div>
                        );
                    })}

                    {groupedDrivers.length === 0 && (
                        <div style={{ padding: '40px', textAlign: 'center', color: '#444' }}>
                            No drivers match your search
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default DriverListModal;
