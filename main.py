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
    Cookie,
    BackgroundTasks
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import security
from models import (
    Item, ItemCreate, ItemUpdate, ItemPublic, ItemResponse, ItemDB,
    Token, TokenData, User, UserInDB
)

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

# ==================== Security Configuration ====================
# This defines the URL where the user will send their username/password
# FastAPI will check for an Authorization header with a Bearer token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": security.get_password_hash("secret"),
        "disabled": False,
    }
}

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Dependency to validate the JWT token and return the current user from the database.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT
        payload = security.jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except security.jwt.JWTError:
        raise credentials_exception
    
    # Fetch user from database
    user = db.query(models.UserDB).filter(models.UserDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Returns the current authenticated user's profile.
    """
    return current_user


def send_welcome_email(email: str):
    """
    Simulates a slow network call (e.g., sending an email).
    """
    print(f"📧 Starting background task: Sending welcome email to {email}...")
    time.sleep(5)
    print(f"✅ Email sent to {email} after 5 seconds.")


@app.post("/signup/", response_model=ItemResponse)
async def signup(email: str, background_tasks: BackgroundTasks):
    """
    Simultates a user signup process.
    The database operation is 'fast', while the email notification is 'slow'.
    The user receives an immediate response while the email is 'sent' in the background.
    """
    # 1. Logic to save user to DB would go here (Simulated fast)
    
    # 2. Add the slow task to the background queue
    background_tasks.add_task(send_welcome_email, email)
    
    # 3. Return response immediately
    return {
        "message": "Signup successful! Check your email in a few moments.",
        "item": None  # We're using ItemResponse structure as requested
    }


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

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Endpoint to exchange username/password for a JWT access token.
    Uses the OAuth2 Password Flow and checks against the database.
    """
    user = db.query(models.UserDB).filter(models.UserDB.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    # Create the token
    access_token = security.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/items/secret")
async def read_secret_items(current_user: Annotated[User, Depends(get_current_user)]):
    """
    A protected route that requires a valid JWT token.
    Validation is handled by the get_current_user dependency.
    """
    return {
        "message": f"Hello {current_user.username}! This is a protected route.",
        "user_details": current_user
    }


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

