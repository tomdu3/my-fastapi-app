# Day 20: Adding a Visual Layer (Jinja2 + StaticFiles)

## Goal
To move beyond raw JSON responses and add a visual interface to the API using **Jinja2 templates** and **static files**. This allows us to serve HTML pages, CSS, and images directly from FastAPI.

## Key Changes

### 1. Dependencies
- Installed `jinja2` (automatically required by Starlette's templating) via `uv add jinja2`.

### 2. Project Structure
Created standard directories for frontend assets:
```text
.
├── static/          # CSS, JS, Images (e.g., style.css, tom_coder.jpg)
├── templates/       # Jinja2 HTML templates (e.g., index.html)
└── main.py
```

### 3. Application Logic (`main.py`)
- **Combined Imports**: Added `StaticFiles` and `Jinja2Templates`.
- **Mounting Static Files**:
  ```python
  app.mount("/static", StaticFiles(directory="static"), name="static")
  ```
- **Template Configuration**:
  ```python
  templates = Jinja2Templates(directory="templates")
  ```
- **New Route**: Added a route to render the template.
  ```python
  @app.get("/welcome/{user_name}")
  async def welcome_user(request: Request, user_name: str):
      return templates.TemplateResponse(
          "index.html",
          {"request": request, "name": user_name}
      )
  ```

### 4. Visual Enhancements (Phase 2)
We didn't just stop at basic HTML. We added some flair:
- **Profile Image**: Added `tom_coder.jpg` displayed with a generic profile class.
- **CSS Animations**:
  - `slideIn`: Exploring entry animations for the main container.
  - `pulseRing`: A concentric circle animation using `box-shadow` to make the profile image pop.
- **Responsive Design**: Applied Mobile-First principles.
  - Used `min-height` for the body.
  - Added `@media (max-width: 600px)` to adjust padding, font sizes, and image dimensions for smaller screens.

## Verification
We verified the implementation by running the server (`uv run uvicorn main:app --port 8001`) and checking:
1.  **HTML Response**: `http://localhost:8001/welcome/Tom` renders the styled page with the image.
2.  **Static Assets**: `http://localhost:8001/static/style.css` and the image load correctly.
3.  **Error Handling**: The custom API exception handler still works for non-existent routes (returning JSON errors), proving that our UI layer doesn't break our API standards.
