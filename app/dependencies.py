from fastapi import Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.schemas.user import User
import app.security as security
from app.config import settings
import time

# ==================== Security Configuration ====================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": security.get_password_hash("secret"),
        "disabled": False,
    }
}

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Dependency to validate the JWT token and return the current user from the database.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT
        payload = security.jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except security.jwt.JWTError:
        raise credentials_exception
    
    # Fetch user from database
    user = db.query(models.UserDB).filter(models.UserDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def send_welcome_email(email: str):
    """
    Simulates a slow network call (e.g., sending an email).
    """
    print(f"📧 Starting background task: Sending welcome email to {email}...")
    time.sleep(5)
    print(f"✅ Email sent to {email} after 5 seconds.")
