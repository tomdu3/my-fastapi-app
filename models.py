from sqlalchemy import Column, Integer, String, Float, Boolean
from pydantic import BaseModel
from database import Base


# ==================== SQLAlchemy Models (Database) ====================

class ItemDB(Base):
    """
    SQLAlchemy model for the items table.
    
    This defines the actual database structure, unlike Pydantic models
    which are used for data validation and API responses.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    tax = Column(Float, nullable=True)


# ==================== Pydantic Models (Schemas) ====================

class Item(BaseModel):
    """Pydantic model for item internal use."""
    id: int | None = None
    name: str
    price: float
    description: str | None = None
    tax: float | None = None


class ItemCreate(BaseModel):
    """Pydantic model for receiving item data via POST."""
    name: str
    price: float
    description: str | None = None
    tax: float | None = None


class ItemUpdate(BaseModel):
    """Pydantic model for receiving partial item data via PATCH."""
    name: str | None = None
    price: float | None = None
    description: str | None = None
    tax: float | None = None


class ItemPublic(BaseModel):
    """Pydantic model for public API responses (hides internal fields)."""
    name: str
    price: float
    description: str | None = None


class ItemResponse(BaseModel):
    """Pydantic model for structured API responses with message."""
    message: str
    item: ItemPublic | None = None


# ==================== Auth Schemas ====================

class UserDB(Base):
    """
    SQLAlchemy model for the users table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

class Token(BaseModel):
    """Schema for returning a JWT token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for the data contained within the JWT."""
    username: str | None = None


class User(BaseModel):
    """Schema for user data."""
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """Schema for user data stored in the database (includes hashed password)."""
    hashed_password: str
