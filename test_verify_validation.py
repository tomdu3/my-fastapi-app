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
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # db has 10 items
    assert len(data) >= 10 
    print(" - Optional query passed")

def test_path_validation():
    print("Testing Path Validation...")
    # Test valid id
    response = client.get("/items/50")
    # Should be 200 (Item found or Item not found, but not 422)
    assert response.status_code == 200, f"Expected 200 for valid ID, got {response.status_code}"
    print(" - Valid ID passed")
    
    # Test too small
    response = client.get("/items/0")
    assert response.status_code == 422, f"Expected 422 for ID=0, got {response.status_code}"
    print(" - ID=0 (too small) passed")
    
    # Test too large
    response = client.get("/items/1001")
    assert response.status_code == 422, f"Expected 422 for ID=1001, got {response.status_code}"
    print(" - ID=1001 (too large) passed")

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
