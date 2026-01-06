from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_query_validation():
    print("Testing Query Validation...")
    # Test valid query (search for "Mouse")
    # Should return a list containing the mouse item
    response = client.get("/items/?q=Mouse")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert isinstance(data, list), "Expected a list of items"
    assert len(data) > 0, "Expected at least one item found"
    assert "Mouse" in data[0]["name"], "Expected 'Mouse' in item name"
    print(" - Valid query passed")

    # Test valid query with no results
    response = client.get("/items/?q=NonExistentItem")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json() == {"message": "No items found"}
    print(" - Valid query (no results) passed")

    # Test too short (min_length=3)
    response = client.get("/items/?q=ab")
    assert response.status_code == 422, f"Expected 422 for short query, got {response.status_code}"
    print(" - Short query passed")

    # Test empty query (optional), should return all items
    response = client.get("/items/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    # db should have items if we are testing, but >= 1 is enough for logic verification
    assert len(data) >= 1, f"Expected at least 1 item, got {len(data)}"
    print(" - Optional query passed")

def test_path_validation():
    print("Testing Path Validation...")
    # Test valid id
    # First, let's create an item if needed, or find an existing one
    response = client.get("/items/")
    items = response.json()
    if isinstance(items, list) and len(items) > 0:
        item_id = items[0]["id"]
    else:
        # Create an item
        create_resp = client.post("/items/", json={"name": "Test Item", "price": 10.0})
        item_id = create_resp.json()["item"]["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, f"Expected 200 for valid ID {item_id}, got {response.status_code}"
    print(f" - Valid ID {item_id} passed")
    
    # Test too small
    response = client.get("/items/0")
    # New implementation returns 404 for any ID not found, as constraints were removed
    assert response.status_code == 404, f"Expected 404 for ID=0, got {response.status_code}"
    print(" - ID=0 (returns 404) passed")
    
    # Test too large
    response = client.get("/items/1001")
    assert response.status_code == 404, f"Expected 404 for ID=1001, got {response.status_code}"
    print(" - ID=1001 (returns 404) passed")

if __name__ == "__main__":
    try:
        test_query_validation()
        test_path_validation()
        print("All tests passed!")
    except AssertionError as e:
        print(f"Test FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
