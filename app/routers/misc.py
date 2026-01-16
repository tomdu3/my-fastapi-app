from fastapi import APIRouter, Request, Form, File, UploadFile, Header, Cookie
from fastapi.templating import Jinja2Templates
from typing import Annotated
from app.config import settings

router = APIRouter(
    tags=["miscellaneous"],
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root():
    return {"message": "Hello World", "version": "2.0"}


@router.get("/info")
async def get_info():
    """
    Demonstrates how to use settings in your application.
    Returns app name and admin email from environment configuration.
    """
    return {"app_name": settings.app_name, "admin": settings.admin_email}


@router.get("/welcome/{user_name}")
async def welcome_user(request: Request, user_name: str):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "name": user_name}
    )


@router.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    """Handle form-based login (not JSON)"""
    return {"username": username}


@router.post("/upload-profile-pic/")
async def upload_image(file: UploadFile = File(...)):
    """Upload a file using UploadFile for memory-efficient handling"""
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }


@router.post("/upload-with-description/")
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


@router.get("/items-user-agent/")
async def read_items_user_agent(
    user_agent: Annotated[str | None, Header()] = None
):
    """Read the User-Agent header from the request"""
    return {"User-Agent": user_agent}


@router.get("/items-header/")
async def read_items_header(
    x_token: Annotated[str, Header(min_length=10)] 
):
    """
    Read a custom X-Token header with validation.
    The token must be at least 10 characters long.
    FastAPI automatically converts x_token to X-Token header.
    """
    return {"X-Token": x_token}


@router.get("/items-cookie/")
async def read_items_cookie(
    ads_id: Annotated[str | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None
):
    """Read cookies from the request (ads_id and session_id)"""
    return {
        "ads_id": ads_id,
        "session_id": session_id
    }
