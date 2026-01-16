from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World", "version": "2.0"}

def test_read_item_no_token():
    # Attempt to access a protected route without a token
    response = client.get("/items/secret")
    assert response.status_code == 401
    assert response.json()["message"] == "Invalid authentication credentials" \
        or response.json()["message"] == "Not authenticated"

def test_404_not_found():
    # Test the Global Exception Handler
    response = client.get("/non-existent-route")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Not Found"
    assert data["path"] == "/non-existent-route"
    assert data["code"] == 404
    assert "timestamp" in data
