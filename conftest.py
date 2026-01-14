import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
import models
import security

# 1. Setup a separate Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_db():
    """
    Create tables at the start of the module and drop them at the end.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests are done
    Base.metadata.drop_all(bind=engine)
    # Optionally remove the file
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def db_session(setup_db):
    """
    Creates a fresh database session for a test.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Returns a TestClient that uses the test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass 

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session):
    """
    Creates a 'johndoe' user in the test database.
    """
    user = models.UserDB(
        username="johndoe",
        email="johndoe@example.com",
        full_name="John Doe",
        hashed_password=security.get_password_hash("secret")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
