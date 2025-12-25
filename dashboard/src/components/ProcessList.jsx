import React from 'react';
import { Activity, Cpu, HardDrive } from 'lucide-react';

const ProcessList = ({ processes }) => {
    if (!processes || processes.length === 0) {
        return (
            <div className="process-list empty">
                <p>No process data available</p>
            </div>
        );
    }

    return (
        <div className="process-list-container">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Activity size={16} color="#F97316" /> Top Processes (by CPU)
            </h3>
            <div className="table-responsive">
                <table className="process-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>PID</th>
                            <th>CPU</th>
                            <th>Memory</th>
                        </tr>
                    </thead>
                    <tbody>
                        {processes.map((proc, index) => (
                            <tr key={`${proc.pid}-${index}`}>
                                <td className="proc-name" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    <div style={{ width: '24px', height: '24px', background: '#222', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                        <HardDrive size={12} color="#aaa" />
                                    </div>
                                    {proc.name}
                                </td>
                                <td className="proc-pid">{proc.pid}</td>
                                <td className="proc-cpu">
                                    <div className="cpu-bar-container">
                                        <div
                                            className="cpu-bar"
                                            style={{ width: `${Math.min(proc.cpu_percent, 100)}%` }}
                                        ></div>
                                        <span>{proc.cpu_percent.toFixed(1)}%</span>
                                    </div>
                                </td>
                                <td className="proc-mem">{proc.memory_percent.toFixed(1)}%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ProcessList;
