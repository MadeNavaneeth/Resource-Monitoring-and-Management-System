import React, { useState, useEffect } from 'react';
import { getAlertSettings, updateAlertSettings } from '../services/api';

const AlertConfigModal = ({ isOpen, onClose, systemId = null }) => {
    const [settings, setSettings] = useState({
        cpu_threshold: 90,
        memory_threshold: 90,
        disk_threshold: 90
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen) {
            loadSettings();
        }
    }, [isOpen, systemId]);

    const loadSettings = async () => {
        try {
            const data = await getAlertSettings(systemId);
            setSettings({
                cpu_threshold: data.cpu_threshold,
                memory_threshold: data.memory_threshold,
                disk_threshold: data.disk_threshold
            });
        } catch (error) {
            console.error("Failed to load settings", error);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setSettings(prev => ({ ...prev, [name]: parseFloat(value) }));
    };

    const handleSave = async (e) => {
        e.preventDefault(); // Keep preventDefault for form submission
        setLoading(true);
        try {
            await updateAlertSettings(settings, systemId);
            onClose();
            alert(`${systemId ? 'System-Specific' : 'Global'} Settings Saved!`);
        } catch (error) {
            console.error("Failed to save settings", error);
            alert("Failed to save.");
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center',
            zIndex: 1000
        }}>
            <div style={{
                backgroundColor: '#0a0a0a', padding: '30px', borderRadius: '12px',
                width: '400px', border: '1px solid #333'
            }}>
                <h2 style={{ margin: '0 0 20px 0', color: '#fff', fontSize: '18px' }}>Configure Alert Thresholds</h2>

                <form onSubmit={handleSave}>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', color: '#aaaaaa', marginBottom: '8px', fontSize: '12px' }}>CPU Threshold (%)</label>
                        <input
                            type="number"
                            name="cpu_threshold"
                            value={settings.cpu_threshold}
                            onChange={handleChange}
                            min="0" max="100"
                            style={{ width: '100%', background: '#111', border: '1px solid #333', color: '#fff', padding: '10px', borderRadius: '4px' }}
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', color: '#aaaaaa', marginBottom: '8px', fontSize: '12px' }}>Memory Threshold (%)</label>
                        <input
                            type="number"
                            name="memory_threshold"
                            value={settings.memory_threshold}
                            onChange={handleChange}
                            min="0" max="100"
                            style={{ width: '100%', background: '#111', border: '1px solid #333', color: '#fff', padding: '10px', borderRadius: '4px' }}
                        />
                    </div>
                    <div style={{ marginBottom: '25px' }}>
                        <label style={{ display: 'block', color: '#aaaaaa', marginBottom: '8px', fontSize: '12px' }}>Disk Threshold (%)</label>
                        <input
                            type="number"
                            name="disk_threshold"
                            value={settings.disk_threshold}
                            onChange={handleChange}
                            min="0" max="100"
                            style={{ width: '100%', background: '#111', border: '1px solid #333', color: '#fff', padding: '10px', borderRadius: '4px' }}
                        />
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                        <button
                            type="button"
                            onClick={onClose}
                            style={{ background: 'transparent', border: '1px solid #333', color: '#aaaaaa', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            style={{ background: '#ff6600', border: 'none', color: '#000', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}
                        >
                            {loading ? 'Saving...' : 'Save Changes'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AlertConfigModal;
