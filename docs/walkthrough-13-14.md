# Day 13 & 14: SQLAlchemy Transition & CRUD — Walkthrough

## 🎯 Goal

Transition from `db.json` to a real **SQLite database** using **SQLAlchemy ORM** and implement full **CRUD operations**.

---

## ✅ What Was Implemented

### 1. Installed SQLAlchemy

```bash
uv add sqlalchemy
```

Added `sqlalchemy==2.0.45` and `greenlet==3.3.0` to the project.

---

### 2. Created Database Configuration

#### [database.py](file:///home/tom/projects/my-fastapi-app/database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

**Key components:**
- `engine` — The database connection with SQLite-specific threading config
- `SessionLocal` — Factory for creating database sessions
- `Base` — Declarative base for all SQLAlchemy models

---

### 3. Created Database Model

#### [models.py](file:///home/tom/projects/my-fastapi-app/models.py)

```python
from sqlalchemy import Column, Integer, String, Float
from database import Base

class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    tax = Column(Float, nullable=True)
```

This maps directly to the existing `Item` Pydantic model structure.

---

### 4. Updated Application Startup

#### [main.py](file:///home/tom/projects/my-fastapi-app/main.py)

Added a **lifespan context manager** to create tables on startup:

```python
from contextlib import asynccontextmanager
from database import engine, Base
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    yield
    print("👋 Application shutting down...")

app = FastAPI(lifespan=lifespan)
```

---

### 5. Updated .gitignore

Added `*.db` to ignore SQLite database files in version control.

---

## 🧪 Verification Results

### Database File Created

```bash
$ ls -la sql_app.db
-rw-r--r-- 1 tom tom 16384 Jan  4 19:59 sql_app.db
```

### Database Schema Verified

```sql
CREATE TABLE items (
    id INTEGER NOT NULL, 
    name VARCHAR, 
    price FLOAT, 
    description VARCHAR, 
    tax FLOAT, 
    PRIMARY KEY (id)
);
CREATE INDEX ix_items_name ON items (name);
CREATE INDEX ix_items_id ON items (id);
```

### API Still Functional

```bash
$ curl http://127.0.0.1:8000/
{"message":"Hello World","version":"2.0"}
```

---

## Day 14: Dependency Injection & CRUD Logic

### 1. Database Session Dependency

In `database.py`, we added the `get_db` generator to handle session lifecycle:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. Migrated Endpoints in `main.py`

All item endpoints now use the `Session` dependency:

```python
@app.get("/items/")
async def read_items(db: Annotated[Session, Depends(get_db)], q: str | None = None):
    query = db.query(ItemDB)
    if q:
        query = query.filter(ItemDB.name.contains(q))
    return query.all()
```

### 3. Model Refactoring

We moved all Pydantic models (`Item`, `ItemPublic`, `ItemResponse`) into `models.py` alongside the SQLAlchemy `ItemDB` model for a cleaner project structure.

---

## 🧪 Verification Results

### Database Operations

1. **POST /items/**: Successfully added "Gaming Mouse" to the SQLite database.
2. **GET /items/**: Successfully retrieved the list of items from the database.
3. **GET /items/1**: Successfully retrieved a specific item with calculated tax.

---

## 📂 Files Changed

| File | Action |
|------|--------|
| [database.py](file:///home/tom/projects/my-fastapi-app/database.py) | **MODIFIED** — Added `get_db` dependency |
| [models.py](file:///home/tom/projects/my-fastapi-app/models.py) | **MODIFIED** — Now contains both SQLAlchemy and Pydantic models |
| [main.py](file:///home/tom/projects/my-fastapi-app/main.py) | **MODIFIED** — Endpoints refactored to use database |
| [.gitignore](file:///home/tom/projects/my-fastapi-app/.gitignore) | **MODIFIED** — Added `*.db` |

---

## 🔮 What's Next (Day 15)

The application is now partially "Production-Ready" with a persistent database. Next steps could involve:
- Adding **Update** and **Delete** endpoints.
- Implementing **Database Migrations** with Alembic.
- Adding Relationships (e.g., Users owning Items).
