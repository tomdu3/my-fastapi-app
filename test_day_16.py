from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_secret_items_no_token():
    """Verify that accessing a protected route without a token returns 401."""
    response = client.get("/items/secret")
    assert response.status_code == 401
    assert response.json()["message"] == "Not authenticated"

def test_read_secret_items_with_token():
    """
    Verify that accessing a protected route with a token returns 200.
    Note: At this stage, we haven't implemented token validation, 
    so any non-empty token should work if provided correctly.
    """
    response = client.get(
        "/items/secret", 
        headers={"Authorization": "Bearer secret-token-123"}
    )
    assert response.status_code == 200
    assert response.json()["token"] == "secret-token-123"
    assert "protected route" in response.json()["message"]

def test_read_secret_items_bad_header():
    """Verify that a malformed Authorization header is rejected."""
    response = client.get(
        "/items/secret", 
        headers={"Authorization": "NotBearer token"}
    )
    assert response.status_code == 401
