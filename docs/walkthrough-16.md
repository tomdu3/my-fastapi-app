# Day 16: Security & OAuth2 Password Flow — Walkthrough

## 🎯 Goal

Introduce the foundation for API security by implementing the **OAuth2 Password Flow** and protecting sensitive endpoints.

---

## ✅ What Was Implemented

### 1. OAuth2 Security Scheme

We integrated FastAPI's built-in security utilities to handle Bearer token authentication.

#### [main.py](file:///home/tom/projects/my-fastapi-app/main.py)

```python
from fastapi.security import OAuth2PasswordBearer

# Defines the path for token acquisition (for Swagger UI)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

The `OAuth2PasswordBearer` utility automatically:
- Searches for the `Authorization` header in requests.
- Validates the format (e.g., `Bearer <token>`).
- Provides a string token to the endpoint if present.

---

### 2. Protected "Secret" Route

We added a new endpoint that requires authentication to access.

#### [main.py](file:///home/tom/projects/my-fastapi-app/main.py)

```python
@app.get("/items/secret")
async def read_secret_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {
        "token": token,
        "message": "This is a protected route! Only authorized users can see this."
    }
```

**Key Highlights:**
- **`Depends(oauth2_scheme)`**: This dependency ensures that the request must contain a valid Authorization head before the function is even called.
- **Routing Order**: We placed this route **before** `/items/{item_id}` to prevent "shadowing" (where a generic route accidentally matches a specific one).

---

### 3. Integrated Security in Swagger UI

By adding the security dependency, FastAPI automatically enhances the interactive documentation:
- **Lock Icons**: Appear next to protected endpoints.
- **"Authorize" Button**: A global button at the top of the `/docs` page allows users to enter their credentials once.

---

## 🧪 Verification Results

We verified the security implementation using `test_day_16.py`.

### Automated Tests Execution

```bash
$ uv run pytest test_day_16.py
========================= 3 passed, 1 warning in 0.75s =========================
```

**Test Cases Covered:**
1. **`test_read_secret_items_no_token`**: Confirmed that requests without a token receive a `401 Unauthorized` response with our custom error format.
2. **`test_read_secret_items_with_token`**: Confirmed that requests with a Bearer token receive a `200 OK` and can see the secret message.
3. **`test_read_secret_items_bad_header`**: Confirmed that malformed Authorization headers (e.g., missing the "Bearer" prefix) are rejected with `401`.

---

## 📂 Files Changed

| File | Action |
|------|--------|
| [main.py](file:///home/tom/projects/my-fastapi-app/main.py) | **MODIFIED** — Added OAuth2 scheme and protected route |
| [test_day_16.py](file:///home/tom/projects/my-fastapi-app/test_day_16.py) | **NEW** — Security verification tests |
| [docs/walkthrough-16.md](file:///home/tom/projects/my-fastapi-app/docs/walkthrough-16.md) | **NEW** — Documentation for Day 16 |

---

## 🔮 What's Next?

Today we set up the **requirement** for a token. In the next phases, we will:
- Implement the actual **`/token`** endpoint to validate usernames and passwords.
- Use **JWT (JSON Web Tokens)** for stateless and secure authentication.
- Hash passwords using **Passlib** and **Bcrypt**.
