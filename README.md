# 🚀 FastAPI 30-Day Project

A production-ready inventory management API built during a 30-day deep dive into FastAPI.

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

This project is the culmination of my **30 Days of FastAPI** challenge. I documented my daily learning and progress on my blog: [**Beyond 400**](https://blog.tomdu3.co.uk/).

## ✨ Features
- **Full CRUD** with PostgreSQL & SQLAlchemy.
- **JWT Authentication** & Password Hashing.
- **Automated Testing** with Pytest (90%+ coverage).
- **Background Tasks** for email notifications.
- **Dockerized** for one-command deployment.

## 🛠️ Setup
1. Install [uv](https://astral.sh/uv).
2. `uv sync`
3. `docker-compose up`
4. Visit `http://localhost:8000/docs`

---

## 📅 The 30-Day Learning Journey

### Phase 1: The Foundations (Days 1–7)
*Focus: Getting up and running with the basics of HTTP and Python type hints.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **01** | **Introduction & Setup** | Install FastAPI and Uvicorn. |
| **02** | **Path Parameters** | Capture variables from the URL. |
| **03** | **Query Parameters** | Handle optional values and pagination. |
| **04** | **Request Body (Pydantic)** | Create data models to validate incoming JSON. |
| **05** | **Query & Path Validation** | Use `Query` and `Path` classes for constraints. |
| **06** | **Response Models** | Filter out sensitive data from the response. |
| **07** | **Status Codes** | Return the correct HTTP status (201, 404, etc.). |

### Phase 2: Mastering Core Features (Days 8–15)
*Focus: Deepening knowledge of data handling and code organization.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **08** | **Handling Errors** | Custom `HTTPException` handlers. |
| **09** | **Dependency Injection** | `Depends()` for shared logic (DB sessions). |
| **10** | **Form Data & Files** | Handle file uploads and form submissions. |
| **11** | **Header & Cookie Params** | Read and validate metadata. |
| **12** | **Background Tasks** | Run "fire and forget" tasks. |
| **13** | **APIRouter** | Organize the app into multiple files. |
| **14** | **Static Files** | Serve CSS, JS, and images. |
| **15** | **Middleware** | Intercept every request (e.g., logging). |

### Phase 3: Databases & Security (Days 16–23)
*Focus: Connecting to the real world and making the API safe.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **16** | **SQLAlchemy Intro** | Connect FastAPI to a SQL database. |
| **17** | **CRUD Operations** | Implement Create, Read, Update, Delete with a DB. |
| **18** | **Database Migrations** | Use **Alembic** to track schema changes. |
| **19** | **SQLModel** | Explore ORM and Pydantic models in one. |
| **20** | **OAuth2 & Passwords** | Implement password hashing and login flows. |
| **21** | **JWT Authentication** | Secure endpoints using JSON Web Tokens. |
| **22** | **CORS & Security** | Configure Cross-Origin Resource Sharing. |
| **23** | **Testing with Pytest** | Write unit tests using `TestClient`. |

### Phase 4: Advanced Topics & Portfolio (Days 24–30)
*Focus: Performance, deployment, and finishing the showcase project.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **24** | **WebSockets** | Build a real-time chat or notification system. |
| **25** | **Async vs. Sync** | Deep dive into `async def` vs. `def`. |
| **26** | **Dockerizing FastAPI** | Create a `Dockerfile` and run in a container. |
| **27** | **Production Servers** | Gunicorn with Uvicorn workers. |
| **28** | **Deployment (Cloud)** | Deploy to platforms like Render or AWS. |
| **29** | **Advanced Documentation** | Customize Swagger UI/ReDoc. |
| **30** | **Portfolio Showcase** | The final architecture and graduation. |

---

## 📚 My Learning Resources
- **Documentation:** [FastAPI Documentation](https://fastapi.tiangolo.com/en/latest/)
- **Course:** [FastAPI – Help You Develop APIs Quickly](https://www.freecodecamp.org/news/fastapi-helps-you-develop-apis-quickly/)
- **Book:** _FastAPI: Modern Python Web Development_ by Bill Lubanovic.
