from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_global_exception_handler_manual_404():
    # This triggers the manual raise HTTPException(status_code=404, detail="Item not found")
    # Must use ID <= 1000 to pass validation
    response = client.get("/items/999")
    print(f"Manual 404 Response: {response.json()}")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Item not found"
    assert data["path"] == "/items/999"
    assert data["code"] == 404
    assert "timestamp" in data

def test_global_exception_handler_route_not_found():
    # This triggers the standard 404 for missing route
    response = client.get("/this-route-does-not-exist")
    print(f"Route Not Found Response: {response.json()}")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    # content detail for standard 404 is usually "Not Found"
    assert data["message"] == "Not Found" 
    assert data["path"] == "/this-route-does-not-exist"
    assert data["code"] == 404
    assert "timestamp" in data

if __name__ == "__main__":
    try:
        test_global_exception_handler_manual_404()
        test_global_exception_handler_route_not_found()
        print("All exception handler tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
