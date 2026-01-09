from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import UserDB
import security
from fastapi.testclient import TestClient
from main import app

# Create tables
Base.metadata.create_all(bind=engine)

def verify_auth():
    db = SessionLocal()
    
    # 1. Create a test user
    username = "testuser"
    password = "testpassword"
    hashed_password = security.get_password_hash(password)
    
    # Check if user already exists
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if not db_user:
        db_user = UserDB(
            username=username,
            email="test@example.com",
            full_name="Test User",
            hashed_password=hashed_password,
            disabled=False
        )
        db.add(db_user)
        db.commit()
        print(f"✅ Created test user: {username}")
    else:
        # Update password just in case
        db_user.hashed_password = hashed_password
        db.commit()
        print(f"ℹ️ Test user {username} already exists, updated password.")
    
    db.close()

    # 2. Test with TestClient
    client = TestClient(app)
    
    # 3. Get token
    print("Testing /token endpoint...")
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    print("✅ Successfully obtained token.")

    # 4. Access /users/me
    print("Testing /users/me endpoint...")
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == username
    print(f"✅ Successfully accessed /users/me: {user_data}")

    # 5. Test invalid token
    print("Testing invalid token...")
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    print("✅ Correctly rejected invalid token (401).")

    print("\n🎉 All authentication tests passed!")

if __name__ == "__main__":
    verify_auth()
