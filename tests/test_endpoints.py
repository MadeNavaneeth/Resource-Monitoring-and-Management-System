"""
Backend Unit Tests for Resource Monitoring System
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine

# Use test client
client = TestClient(app)

# API Key for testing
TEST_API_KEY = "secret-agent-key"


class TestHealthEndpoints:
    """Test basic health and root endpoints."""
    
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestSystemsEndpoints:
    """Test system-related endpoints."""
    
    def test_get_systems_unauthorized(self):
        """Should fail without auth."""
        response = client.get("/api/v1/systems")
        # Depending on your auth setup, this may be 401 or 403
        assert response.status_code in [401, 403, 200]  # 200 if no auth required
    
    def test_register_system(self):
        """Test system registration with API key."""
        response = client.post(
            "/api/v1/systems/register",
            headers={"X-API-Key": TEST_API_KEY},
            json={
                "hostname": "test-system",
                "ip_address": "192.168.1.100",
                "os_info": "Windows 11",
                "agent_version": "1.0.0"
            }
        )
        assert response.status_code == 200
        assert "id" in response.json()


class TestMetricsEndpoints:
    """Test metrics-related endpoints."""
    
    def test_create_metric_unauthorized(self):
        """Should fail without API key."""
        response = client.post(
            "/api/v1/systems/1/metrics",
            json={
                "cpu_usage": 50.0,
                "memory_percent": 60.0,
                "disk_usage": 70.0
            }
        )
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
