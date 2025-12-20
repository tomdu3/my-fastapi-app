# My FastAPI App

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

This is a simple FastAPI app that I use in the challenge of 30 Days of FastAPI.

---

## 🚀 30 Days of FastAPI: Learning Schedule

### 📅 Phase 1: The Foundations (Days 1–7)

*Focus: Getting up and running with the basics of HTTP and Python type hints.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **01** | **Introduction & Setup** | Install FastAPI and Uvicorn; run your first "Hello World". |
| **02** | **Path Parameters** | Capture variables from the URL (e.g., `/items/{item_id}`). |
| **03** | **Query Parameters** | Handle optional values and pagination (e.g., `?skip=0&limit=10`). |
| **04** | **Request Body (Pydantic)** | Create data models to validate incoming JSON data. |
| **05** | **Query & Path Validation** | Use `Query` and `Path` classes to add constraints like `min_length`. |
| **06** | **Response Models** | Filter out sensitive data from the response using `response_model`. |
| **07** | **Status Codes** | Return the correct HTTP status (201 Created, 404 Not Found, etc.). |

---

### 📅 Phase 2: Mastering Core Features (Days 8–15)

*Focus: Deepening your knowledge of data handling and code organization.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **08** | **Handling Errors** | Create custom `HTTPException` handlers for consistent API responses. |
| **09** | **Dependency Injection** | Learn the basics of `Depends()` for shared logic (e.g., database sessions). |
| **10** | **Form Data & Files** | Handle file uploads and form submissions using `File` and `UploadFile`. |
| **11** | **Header & Cookie Params** | Read and validate metadata from request headers and cookies. |
| **12** | **Background Tasks** | Run "fire and forget" tasks after returning a response. |
| **13** | **APIRouter** | Organize your app into multiple files as it grows larger. |
| **14** | **Static Files** | Serve CSS, JS, and images for mini-frontends. |
| **15** | **Middleware** | Intercept every request (e.g., for logging execution time). |

---

### 📅 Phase 3: Databases & Security (Days 16–23)

*Focus: Connecting to the real world and making your API safe.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **16** | **SQLAlchemy Intro** | Connect FastAPI to a SQL database (SQLite/PostgreSQL). |
| **17** | **CRUD Operations** | Implement Create, Read, Update, and Delete logic with a DB. |
| **18** | **Database Migrations** | Use **Alembic** to track changes in your database schema. |
| **19** | **SQLModel** | Explore the "FastAPI-native" way to do ORM and Pydantic models in one. |
| **20** | **OAuth2 & Passwords** | Implement password hashing and basic login flows. |
| **21** | **JWT Authentication** | Secure your endpoints using JSON Web Tokens. |
| **22** | **CORS & Security** | Configure Cross-Origin Resource Sharing for frontend access. |
| **23** | **Testing with Pytest** | Write unit tests for your endpoints using `TestClient`. |

---

### 📅 Phase 4: Advanced Topics & Portfolio (Days 24–30)

*Focus: Performance, deployment, and finishing your showcase project.*

| Day | Topic | Learning Goal |
| --- | --- | --- |
| **24** | **WebSockets** | Build a real-time chat or notification system. |
| **25** | **Async vs. Sync** | Deep dive into when to use `async def` vs. normal `def`. |
| **26** | **Dockerizing FastAPI** | Create a `Dockerfile` and run your app in a container. |
| **27** | **Production Servers** | Configure Gunicorn with Uvicorn workers for high performance. |
| **28** | **Deployment (Cloud)** | Deploy your app to platforms like Render, Railway, or AWS. |
| **29** | **Advanced Documentation** | Customize Swagger UI/ReDoc with metadata and logos. |
| **30** | **Portfolio Showcase** | Combine everything into a final project (e.g., a Task Manager or Movie API). |

---
## 📚 My Learning Resources

I’ll be sticking to these high-quality resources to guide my 30-day sprint:

- **Documentation:** [FastAPI Documentation](https://fastapi.tiangolo.com/en/latest/)

-   **Course:** [FastAPI – Help You Develop APIs Quickly](https://www.freecodecamp.org/news/fastapi-helps-you-develop-apis-quickly/) by Beau Carnes (FreeCodeCamp).
    
-   **Book:** _FastAPI: Modern Python Web Development_ by Bill Lubanovic (O’Reilly).
