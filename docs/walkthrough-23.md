# Walkthrough 23: Security and Configuration Management

**Date:** 2026-01-15  
**Topic:** Implementing Pydantic Settings for environment-based configuration

## Overview

Today we moved the project from "hobbyist" to "professional" by implementing proper configuration management using Pydantic Settings and `.env` files. This protects sensitive data like `SECRET_KEY` and makes the application configurable for different environments.

## What Changed

### 1. Installed pydantic-settings

```bash
uv add pydantic-settings
```

This installed:
- `pydantic-settings==2.12.0`
- `python-dotenv==1.2.1` (dependency)

### 2. Created Configuration Files

#### [config.py](file:///home/tom/projects/my-fastapi-app/config.py)
Created a new `Settings` class that:
- Inherits from `BaseSettings` for type-safe configuration
- Defines all application settings with proper types
- Provides sensible defaults where appropriate
- Reads from `.env` file automatically

Configuration fields:
- `app_name`: Application name (default: "My FastAPI App")
- `admin_email`: Admin contact email (required)
- `items_per_user`: Maximum items per user (default: 20)
- `secret_key`: JWT signing key (required)
- `database_url`: SQLAlchemy database URL (default: "sqlite:///./sql_app.db")
- `algorithm`: JWT algorithm (default: "HS256")
- `access_token_expire_minutes`: Token expiration time (default: 30)

#### [.env](file:///home/tom/projects/my-fastapi-app/.env)
Created environment file with actual configuration values:
```env
ADMIN_EMAIL="admin@example.com"
SECRET_KEY="your-super-ultra-secret-key-change-this-in-production"
ITEMS_PER_USER=50
```

> [!CAUTION]
> The `.env` file contains sensitive secrets and is now protected by `.gitignore` to prevent accidental commits.

#### [.env.example](file:///home/tom/projects/my-fastapi-app/.env.example)
Created a template file for other developers showing all available configuration options with example values.

### 3. Updated Existing Files

#### [security.py](file:///home/tom/projects/my-fastapi-app/security.py)
**Removed** hardcoded constants:
```diff
-SECRET_KEY = "your-super-secret-key-here"
-ALGORITHM = "HS256"
-ACCESS_TOKEN_EXPIRE_MINUTES = 30
+from config import settings
```

**Updated** `create_access_token()` to use settings:
```diff
-expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
-encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
+expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
+encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
```

#### [database.py](file:///home/tom/projects/my-fastapi-app/database.py)
**Removed** hardcoded database URL:
```diff
-SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
-engine = create_engine(SQLALCHEMY_DATABASE_URL, ...)
+from config import settings
+engine = create_engine(settings.database_url, ...)
```

#### [main.py](file:///home/tom/projects/my-fastapi-app/main.py)
**Added** settings import and updated JWT decoding:
```diff
+from config import settings

 payload = security.jwt.decode(
-    token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
+    token, settings.secret_key, algorithms=[settings.algorithm]
 )
```

**Added** new `/info` endpoint to demonstrate settings usage:
```python
@app.get("/info")
async def get_info():
    """Returns app name and admin email from environment configuration."""
    return {"app_name": settings.app_name, "admin": settings.admin_email}
```

#### [.gitignore](file:///home/tom/projects/my-fastapi-app/.gitignore)
**Added** `.env` to prevent committing secrets:
```gitignore
# Environment variables
.env
```

#### [test_db_isolation.py](file:///home/tom/projects/my-fastapi-app/test_db_isolation.py)
**Updated** test to use settings instead of removed constant:
```diff
-from database import SQLALCHEMY_DATABASE_URL as PROD_DATABASE_URL
+from config import settings
+import sqlite3

-prod_db_path = PROD_DATABASE_URL.replace("sqlite:///./", "")
+prod_db_path = settings.database_url.replace("sqlite:///./", "")
```

### 4. Updated `.gitignore`

Confirmed that `.env` is now ignored by git:
```bash
$ git status
# .env is NOT listed in untracked files ✅
```

## Testing Results

### All Tests Pass ✅

```bash
$ uv run pytest -v
================== test session starts ===================
collected 5 items

test_db_isolation.py::test_db_isolation PASSED     [ 20%]
test_db_isolation.py::test_test_db_creation PASSED [ 40%]
test_main.py::test_read_main PASSED                [ 60%]
test_main.py::test_read_item_no_token PASSED       [ 80%]
test_main.py::test_404_not_found PASSED            [100%]

============= 5 passed, 3 warnings in 0.20s ==============
```

### Settings Loading Verification

Verified settings are loaded correctly from `.env`:
```bash
$ uv run python -c "from config import settings; print(settings.app_name)"
My FastAPI App
```

## How to Use Settings

### In Any Module

Simply import the settings singleton:
```python
from config import settings

# Access configuration values
print(settings.secret_key)
print(settings.database_url)
print(settings.admin_email)
```

### Environment Priority

Settings are loaded in this order:
1. **Environment variables** (highest priority)
2. **`.env` file**
3. **Default values** in Settings class

Example:
```bash
# Override via environment variable
export SECRET_KEY="production-secret-key"
uvicorn main:app

# Or use .env file (already configured)
uvicorn main:app
```

## New Endpoint

### GET /info

Returns application configuration (non-sensitive data):

**Request:**
```bash
curl http://localhost:8000/info
```

**Response:**
```json
{
  "app_name": "My FastAPI App",
  "admin": "admin@example.com"
}
```

## Benefits Achieved

✅ **Security**: Secrets are no longer hardcoded in source files  
✅ **Git Safety**: `.env` is ignored, preventing accidental commits  
✅ **Type Safety**: Pydantic validates configuration types  
✅ **Flexibility**: Easy to configure different environments (dev/test/prod)  
✅ **Documentation**: `.env.example` provides clear template for team  
✅ **Maintainability**: Centralized configuration in one place

## Next Steps

To prepare for production, you should:
1. Generate a strong `SECRET_KEY` using a cryptographic tool
2. Update `SECRET_KEY` in your `.env` file
3. Configure production `DATABASE_URL` (e.g., PostgreSQL)
4. Never commit your `.env` file to version control

## Summary

This implementation transitions the project from hardcoded values to professional configuration management. The application now reads sensitive data from environment variables, making it safe to share code publicly and easy to configure for different deployment environments.
