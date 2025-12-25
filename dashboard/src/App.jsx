import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import SystemDetail from './pages/SystemDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import ErrorBoundary from './components/ErrorBoundary';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (loading) {
    return <div className="loading">Initializing</div>;
  }

  return (
    <ErrorBoundary>
      <Router>
        <div className="app">
          {isAuthenticated ? (
            <>
              <Navbar onLogout={handleLogout} />
              <main className="main-content">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/system/:id" element={<SystemDetail />} />
                  <Route path="*" element={<Navigate to="/" />} />
                </Routes>
              </main>
              <footer className="app-footer">
                <span>SysMonitor v1.0.0</span>
                <span>•</span>
                <span>Real-time Resource Monitoring</span>
              </footer>
            </>
          ) : (
            <Routes>
              <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
              <Route path="/register" element={<Register />} />
              <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
          )}
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;

