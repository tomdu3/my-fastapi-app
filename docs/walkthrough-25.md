# Walkthrough - Day 25: Dockerizing FastAPI with uv

I have successfully containerized the FastAPI application using `uv`. This ensures a consistent environment and optimized build performance.

## Changes Made

### Docker Configuration
- Created [.dockerignore](file:///home/tom/projects/my-fastapi-app/.dockerignore) to exclude unnecessary files like `.env`, `.venv`, and `*.db`.
- Created [Dockerfile](file:///home/tom/projects/my-fastapi-app/Dockerfile) using a multi-stage approach to include `uv` and optimize dependency caching.

### Dependency Management
- Added `bcrypt` to `pyproject.toml` and pinned it to version `<4.0.0` (3.2.2) to resolve a compatibility issue with `passlib` on Python 3.11+.
- Updated `uv.lock` with the new dependencies.

## Verification Results

### Docker Build
The image was built successfully using `uv sync --frozen --no-dev`, which provides extremely fast dependency installation.

```bash
docker build -t my-fastapi-app .
```

### Container Execution
The container was verified by running it with an environment file and checking the health endpoint.

```bash
docker run -d --name test-fastapi-app --env-file .env -p 8000:8000 my-fastapi-app
curl -I http://localhost:8000/docs
# Response: HTTP/1.1 200 OK
```

### Challenges Resolved
- **Missing Dependency**: Initially, `bcrypt` was missing as a direct dependency.
- **Library Incompatibility**: The latest `bcrypt` version (5.0.0) caused a crash due to `passlib` trying to access non-existent attributes. Pinning `bcrypt<4.0.0` fixed this.
- **Build Cache**: Adjusted `.dockerignore` to ensure `uv.lock` is available for `uv sync` while keeping the image size small.
