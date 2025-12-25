import axios from 'axios';

const API_URL = 'http://172.24.126.24:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      // Redirect to login if not already there
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth
export const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

export const register = async (email, password) => {
  const response = await api.post('/auth/register', { email, password });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/me');
  return response.data;
};

// Systems
export const getSystems = async () => {
  const response = await api.get('/systems');
  return response.data;
};

export const getSystem = async (systemId) => {
  const response = await api.get(`/systems/${systemId}`);
  return response.data;
};

export const deleteSystem = async (systemId) => {
  const response = await api.delete(`/systems/${systemId}`);
  return response.data;
};

// Metrics
export const getMetrics = async (systemId, limit = 100) => {
  const response = await api.get(`/metrics/${systemId}?limit=${limit}`);
  return response.data;
};

export const exportMetrics = async (systemId) => {
  const response = await api.get(`/metrics/${systemId}/export`, {
    responseType: 'blob', // Important for file download
  });
  return response; // Return full response to access headers if needed, or just data
};

// Alerts
export const getAlerts = async (isResolved = false) => {
  const response = await api.get('/alerts', { params: { is_resolved: isResolved } });
  return response.data;
};

export const resolveAlert = async (alertId) => {
  const response = await api.put(`/alerts/${alertId}/resolve`);
  return response.data;
};

// Tickets
export const getTickets = async (systemId) => {
  const response = await api.get(`/tickets`, { params: { system_id: systemId } });
  return response.data;
};

export const updateTicketStatus = async (ticketId, status) => {
  const response = await api.put(`/tickets/${ticketId}/status`, { status });
  return response.data;
};

// Alert Settings
export const getAlertSettings = async (systemId = null) => {
  const params = {};
  if (systemId) params.system_id = systemId;
  const response = await api.get('/alerts/settings', { params });
  return response.data;
};

export const updateAlertSettings = async (settings, systemId = null) => {
  const payload = { ...settings };
  if (systemId) payload.system_id = systemId;
  const response = await api.put('/alerts/settings', payload);
  return response.data;
};

export default api;
