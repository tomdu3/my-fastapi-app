import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime

from app.database import engine, Base
from app.routers import items, users, misc

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

# ==================== Database Initialization ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for database initialization.
    Creates all database tables on startup.
    """
    # Startup: Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully!")
    yield
    # Shutdown: Cleanup (if needed)
    logger.info("👋 Application shutting down...")


app = FastAPI(
    title="Inventory Master API",
    description="""
    A high-performance API for managing global inventories.
    
    ## Items
    You can **read** and **create** items.
    
    ## Users
    You can **register** and **manage** profiles.
    """,
    version="1.0.2",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "support@example.com",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "items",
            "description": "Manage items. So _fancy_ they have their own docs.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
        {
            "name": "auth",
            "description": "Authentication and authorization operations.",
        },
        {
            "name": "miscellaneous",
            "description": "Miscellaneous helper endpoints.",
        },
    ],
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== CORS Configuration ====================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://my-production-app.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Custom Middleware ====================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    # Log details as a structured-like message
    logger.info(
        f"method={request.method} path={request.url.path} "
        f"status={response.status_code} duration={process_time:.2f}ms"
    )
    
    # Keep the custom header for backward compatibility
    response.headers["X-Process-Time"] = f"{process_time / 1000:.4f}s"
    
    return response

# ==================== Exception Handlers ====================
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Log the error before returning the response
    logger.error(f"HTTP Error: {exc.detail} path={request.url.path} code={exc.status_code}")
    
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

# ==================== Include Routers ====================
app.include_router(users.router)
app.include_router(users.user_router)
app.include_router(items.router)
app.include_router(misc.router)
