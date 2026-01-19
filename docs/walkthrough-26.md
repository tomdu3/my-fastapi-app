# Day 26: Docker Compose & PostgreSQL — The Production Stack

## Goal
Transition the FastAPI application from a single local SQLite database to a multi-container architecture using Docker Compose and PostgreSQL.

## Implementation Details

### 1. Dependencies
We added `psycopg2-binary` to the project to enable Python to communicate with PostgreSQL.

```bash
uv add psycopg2-binary
```

### 2. Docker Compose Configuration
Created `docker-compose.yml` to define two services:
- **`db`**: The PostgreSQL database service using the `postgres:15-alpine` image. It persists data using a named volume `postgres_data`.
- **`api`**: The FastAPI application service. It depends on `db` and connects via the `DATABASE_URL` environment variable.

**Key File:** `docker-compose.yml`
```yaml
services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=fastapi_db

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/fastapi_db
    depends_on:
      - db
    env_file:
      - .env

volumes:
  postgres_data:
```

### 3. Database Connection Logic
Updated `app/database.py` to handle the connection string dynamically. SQLite requires `check_same_thread=False`, but PostgreSQL does not.

**Key Change in `app/database.py`:**
```python
connect_args = {}
if "sqlite" in settings.database_url:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url, connect_args=connect_args
)
```

## Verification Steps

### Step 1: Start the Stack
Run the following command to build the image and start the containers in detached mode:
```bash
docker compose up --build -d
```
*Expected Output:* `api` and `db` services start successfully.

### Step 2: Verify API Availability
Check if the API documentation is accessible:
```bash
curl -I http://localhost:8000/docs
```
*Expected Result:* `HTTP/1.1 200 OK`

### Step 3: Verify Database Tables
The application is configured to create tables on startup (`Base.metadata.create_all`). We verified this by connecting directly to the running Postgres container:

```bash
docker compose exec db psql -U user -d fastapi_db -c '\dt'
```

*Output:*
```text
       List of relations
 Schema | Name  | Type  | Owner 
--------+-------+-------+-------
 public | items | table | user
 public | users | table | user
(2 rows)
```

This confirms that the application successfully connected to the PostgreSQL database and created the schema.
