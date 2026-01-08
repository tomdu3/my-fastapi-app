from fastapi.testclient import TestClient
from main import app
import security
from datetime import timedelta
import pytest

client = TestClient(app)

def test_password_hashing():
    password = "testpassword"
    hashed = security.get_password_hash(password)
    assert hashed != password
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrongpassword", hashed)

def test_create_access_token():
    data = {"sub": "testuser"}
    token = security.create_access_token(data)
    assert token
    
    payload = security.jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "exp" in payload

def test_token_endpoint():
    # Valid credentials
    response = client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Invalid credentials
    response = client.post(
        "/token",
        data={"username": "johndoe", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Incorrect username or password"

def test_protected_route():
    # Login to get token
    response = client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"}
    )
    token = response.json()["access_token"]

    # Access protected route with token
    response = client.get(
        "/items/secret",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Hello johndoe! This is a protected route."

    # Access protected route without token
    response = client.get("/items/secret")
    assert response.status_code == 401

    # Access protected route with invalid token
    response = client.get(
        "/items/secret",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
