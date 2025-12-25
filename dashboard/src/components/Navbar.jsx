import React from 'react';
import { Link } from 'react-router-dom';
import { LayoutDashboard, Server, LogOut } from 'lucide-react';

const Navbar = ({ onLogout }) => {
    return (
        <nav className="navbar">
            <div className="container">
                <Link to="/" className="logo">
                    <Server size={22} />
                    <span>SysMonitor</span>
                    <span className="live-indicator" title="Live - 1 second updates">
                        <span className="live-dot"></span>
                        LIVE
                    </span>
                </Link>
                <div className="links">
                    <Link to="/" className="nav-link">
                        <LayoutDashboard size={16} />
                        Dashboard
                    </Link>
                    <button onClick={onLogout} className="logout-btn">
                        <LogOut size={14} /> Logout
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

