import time
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    Path,
    Query,
    HTTPException,
    Request,
    Depends,
    Form,
    File,
    UploadFile,
    Header,
    Cookie
)
from fastapi.middleware.cors import CORSMiddleware

from typing import Annotated
from fastapi.responses import JSONResponse
from starlette.exceptions import (
    HTTPException as StarletteHTTPException
)
from datetime import datetime
import json
from sqlalchemy.orm import Session
# SQLAlchemy imports
from database import engine, Base, get_db
from models import Item, ItemCreate, ItemUpdate, ItemPublic, ItemResponse, ItemDB
import models  # noqa: F401 - Import models to register them with Base


# ==================== Database Initialization ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for database initialization.
    Creates all database tables on startup.
    """
    # Startup: Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    yield
    # Shutdown: Cleanup (if needed)
    print("👋 Application shutting down...")


app = FastAPI(lifespan=lifespan)


# ==================== CORS Configuration ====================
# List of allowed origins for cross-origin requests
origins = [
    "http://localhost:3000",      # React/Next.js dev server
    "http://localhost:5173",      # Vite dev server
    "https://my-production-app.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ==================== Custom Middleware ====================
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware that adds X-Process-Time header to every response.
    This helps monitor API performance and identify slow endpoints.
    """
    start_time = time.time()
    
    # The request goes "down" into the path operation
    response = await call_next(request)
    
    # The response comes "up" back through the middleware
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    
    return response

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": request.url.path,
            "code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        },
    )


# Pydantic models are now imported from models.py
# - Item: for item creation and internal use
# - ItemPublic: for public API responses
# - ItemResponse: for structured API responses

# Database logic has been moved to database.py and models.py
# The local db.json file has been retired.


@app.get("/")
async def read_root():
    return {"message": "Hello World", "version": "2.0"}


@app.get("/items/")
async def read_items(
    db: Annotated[Session, Depends(get_db)],
    q: str | None = Query(
        None,
        min_length=3,
        max_length=50,
        title="Search Query",
        description="Search for items in the database",
    )
):
    query = db.query(ItemDB)
    if q:
        query = query.filter(ItemDB.name.contains(q))
    
    results = query.all()
    if not results:
        return {"message": "No items found"}
    return results


@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # 1. Create the DB object
    db_item = models.ItemDB(**item.dict())
    # 2. Add and Commit
    db.add(db_item)
    db.commit()
    # 3. Refresh to get the generated ID
    db.refresh(db_item)
    return {"message": "Item created", "item": db_item}

# returns a pydantic model for the response
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    # 1. Find the item
    db_item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # 2. Update only the fields provided
    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    # 3. Save and return
    db.commit()
    db.refresh(db_item)
    return {"message": "Item updated", "item": db_item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}


# Form Data and File Uploads
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    """Handle form-based login (not JSON)"""
    return {"username": username}


@app.post("/upload-profile-pic/")
async def upload_image(file: UploadFile = File(...)):
    """Upload a file using UploadFile for memory-efficient handling"""
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }


@app.post("/upload-with-description/")
async def upload_with_description(
    description: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload a file along with form field data (multipart request)"""
    contents = await file.read()
    return {
        "description": description,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

# Header and Cookie Parameters
@app.get("/items-user-agent/")
async def read_items_user_agent(
    user_agent: Annotated[str | None, Header()] = None
):
    """Read the User-Agent header from the request"""
    return {"User-Agent": user_agent}


@app.get("/items-header/")
async def read_items_header(
    x_token: Annotated[str, Header(min_length=10)] 
):
    """
    Read a custom X-Token header with validation.
    The token must be at least 10 characters long.
    FastAPI automatically converts x_token to X-Token header.
    """
    return {"X-Token": x_token}


@app.get("/items-cookie/")
async def read_items_cookie(
    ads_id: Annotated[str | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None
):
    """Read cookies from the request (ads_id and session_id)"""
    return {
        "ads_id": ads_id,
        "session_id": session_id
    }

