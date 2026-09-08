"""Test FastAPI endpoints."""
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    
def test_recommend_endpoint():
    """Test recommend endpoint."""
    response = client.post("/recommend?resource_id=test&utilization=5")
    assert response.status_code == 200
    assert "annual_savings" in response.json()
    
def test_recommend_no_recommendation():
    """Test recommend endpoint with high utilization."""
    response = client.post("/recommend?resource_id=test&utilization=80")
    assert response.status_code == 200
    assert "message" in response.json()
    