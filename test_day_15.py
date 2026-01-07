from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_crud_lifecycle():
    # 1. Create an item
    create_payload = {
        "name": "Test Item",
        "price": 10.5,
        "description": "A test item",
        "tax": 1.5
    }
    response = client.post("/items/", json=create_payload)
    assert response.status_code == 201
    item_id = response.json()["item"]["name"] # Wait, ItemResponse.item is ItemPublic which has name, price, description but NOT ID.
    # Ah, I should check the implementation of create_item in main.py
    # return {"message": "Item created", "item": db_item}
    # ItemDB has id. ItemResponse.item is ItemPublic.
    # Let me check models.py again.
    # class ItemPublic(BaseModel): name, price, description.
    # class ItemResponse(BaseModel): message, item: ItemPublic | None
    
    # Wait, if ItemResponse.item is ItemPublic, it won't have the ID.
    # I should probably check if I should add ID to ItemPublic or if I should return the whole DB item in a different field.
    # Usually we want the ID back.
    
    # Let me look at main.py:143: return {"message": "Item created", "item": db_item}
    # Since response_model=ItemResponse, FastAPI will filter db_item through ItemResponse.
    # ItemResponse.item is ItemPublic. ItemPublic does NOT have id.
    
    # Let me check read_item: return item. It doesn't have a response_model, so it returns everything.
    
    # I'll create the item and then get all items to find the ID, or just use read_item if I can guess the ID (if it's the only one).
    # Better yet, I'll update ItemPublic to include ID if it makes sense, but maybe I should just test without ID if I can't get it easily.
    
    # Actually, let me just check the full response from POST without response_model filtering if I were to remove it, 
    # but I should stick to the requested implementation.
    
    # I'll fetch all items and find the one I just created.
    get_all = client.get("/items/")
    assert get_all.status_code == 200
    items = get_all.json()
    item = next(i for i in items if i["name"] == "Test Item")
    item_id = item["id"]

    # 2. Partial Update (PATCH)
    update_payload = {"price": 15.0}
    patch_response = client.patch(f"/items/{item_id}", json=update_payload)
    assert patch_response.status_code == 200
    assert patch_response.json()["item"]["price"] == 15.0
    assert patch_response.json()["item"]["name"] == "Test Item" # Should remain unchanged

    # 3. Verify update in database
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["price"] == 15.0

    # 4. Delete the item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Item deleted successfully"

    # 5. Verify deletion
    get_deleted = client.get(f"/items/{item_id}")
    assert get_deleted.status_code == 404

def test_patch_non_existent():
    response = client.patch("/items/999999", json={"name": "Non-existent"})
    assert response.status_code == 404
    assert response.json()["message"] == "Item not found"

def test_delete_non_existent():
    response = client.delete("/items/999999")
    assert response.status_code == 404
    assert response.json()["message"] == "Item not found"
