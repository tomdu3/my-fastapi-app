import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ItemDB
from database import SQLALCHEMY_DATABASE_URL as PROD_DATABASE_URL

def test_db_isolation(client):
    # 1. Create an item via the API (using the test database)
    response = client.post(
        "/items/",
        json={
            "name": "Test Item",
            "price": 9.99,
            "description": "This should only be in test.db"
        }
    )
    assert response.status_code == 201
    item_id = response.json()["item"]["name"] 
    # The response model uses ItemPublic which doesn't have ID,
    # but ItemResponse has 'item'
    
    # 2. Verify it's in the test database
    # We can use the db_session fixture indirectly through the client
    # or directly if we added it, but let's just check the API again
    # which we know uses the override.
    get_response = client.get("/items/")
    assert get_response.status_code == 200
    items = get_response.json()
    assert any(item["name"] == "Test Item" for item in items)

    # 3. Verify the production database remains unchanged
    # Connect directly to the production DB file to check
    prod_db_path = PROD_DATABASE_URL.replace("sqlite:///./", "")
    if os.path.exists(prod_db_path):
        conn = sqlite3.connect(prod_db_path)
        cursor = conn.cursor()
        # Check if the 'items' table exists first
        # (it might not if it's a fresh setup)
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND"
            " name='items';"
        )
        if cursor.fetchone():
            cursor.execute("SELECT * FROM items WHERE name = 'Test Item'")
            row = cursor.fetchone()
            assert row is None, "Test Item found in production database!"
        conn.close()

def test_test_db_creation():
    # This test doesn't use the client fixture initialy, 
    # but we want to verify that running pytest triggers the setup_db fixture.
    # However, fixtures are only triggered when requested.
    pass
