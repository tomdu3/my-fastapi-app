# Database Testing Walkthrough

We have successfully implemented a professional testing strategy using a dedicated **Test Database** and **Pytest Fixtures**. This setup ensures that our tests run against a clean, isolated environment without interfering with the production data.

## Key Accomplishments

### 1. Dedicated Test Database
Updated `conftest.py` to use `sqlite:///./test.db` instead of an in-memory database. This allows for better simulation of a real-world disk-based database while still being isolated.

### 2. Module-Scoped Fixture
Implemented the `setup_db` fixture with `scope="module"`. This fixture handles the creation and destruction of the database tables once per test module, making the test suite faster while maintaining a clean state.

```python
@pytest.fixture(scope="module")
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests are done
    Base.metadata.drop_all(bind=engine)
    # Cleanup the file
    if os.path.exists("./test.db"):
        os.remove("./test.db")
```

### 3. Dependency Overriding
Modified the `client` fixture to override the `get_db` dependency in FastAPI. This ensures that every request made through the `TestClient` uses the test database session.

```python
def override_get_db():
    try:
        yield db_session
    finally:
        pass 

app.dependency_overrides[get_db] = override_get_db
```

## Verification Results

### Automated Tests
Ran `uv run pytest` which executed all tests, including the new isolation test.

**Results:**
- `test_db_isolation.py`: PASSED
- `test_main.py`: PASSED

### Isolation Confirmation
The `test_db_isolation(client)` test explicitly verified:
1. An item created via the API exists in the test database.
2. The same item **does not exist** in the production `sql_app.db`.

```python
# From test_db_isolation.py
if cursor.fetchone():
    cursor.execute("SELECT * FROM items WHERE name = 'Test Item'")
    row = cursor.fetchone()
    assert row is None, "Test Item found in production database!"
```

## Conclusion
Our testing suite is now robust, isolated, and follows FastAPI best practices. The "Dirty Data" problem is solved!
