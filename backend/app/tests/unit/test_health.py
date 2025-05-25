"""
Unit tests for health endpoint

Following test-driven development principles:
1. Write tests first
2. Implement to make tests pass
3. Refactor while keeping tests green
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestHealthEndpoint:
    """Test suite for health endpoint functionality."""
    
    def setup_method(self):
        """Set up test client for each test method."""
        self.client = TestClient(app)
    
    def test_health_endpoint_exists(self):
        """Test that health endpoint is accessible."""
        response = self.client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self):
        """Test that health endpoint returns JSON content."""
        response = self.client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_response_structure(self):
        """Test that health endpoint returns expected structure."""
        response = self.client.get("/health")
        data = response.json()
        
        # Verify required fields are present
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "service" in data
    
    def test_health_endpoint_status_healthy(self):
        """Test that health endpoint indicates healthy status."""
        response = self.client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "mabos-backend"
    
    def test_health_endpoint_performance(self):
        """Test that health endpoint responds quickly."""
        import time
        start_time = time.time()
        response = self.client.get("/health")
        end_time = time.time()
        
        # Health check should respond in under 1 second
        assert (end_time - start_time) < 1.0
        assert response.status_code == 200 