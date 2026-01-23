from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.schemas.user import Token, User, UserInDB
from app.schemas.item import ItemResponse
import app.security as security
from app.config import settings
from app.dependencies import get_current_user, send_welcome_email

from app.repositories import UserRepository

router = APIRouter(
    tags=["auth"],
)

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Endpoint to exchange username/password for a JWT access token.
    Uses the OAuth2 Password Flow and checks against the database.
    """
    repo = UserRepository(db)
    user = repo.get_by_username(form_data.username)
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


@user_router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Returns the current authenticated user's profile.
    """
    return current_user


@router.post("/signup/", response_model=ItemResponse)
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
