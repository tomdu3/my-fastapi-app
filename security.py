from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a plain-text password."""
    # Bcrypt has a 72-byte limit. We truncate to ensure compatibility
    # and avoid ValueError from the bcrypt backend.
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a plain-text password matches a hashed version."""
    return pwd_context.verify(plain_password[:72], hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generates a JWT token with an optional expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

