from sqlalchemy import Column, Integer, String, Float
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


class ItemPublic(BaseModel):
    """Pydantic model for public API responses (hides internal fields)."""
    name: str
    price: float
    description: str | None = None


class ItemResponse(BaseModel):
    """Pydantic model for structured API responses with message."""
    message: str
    item: ItemPublic | None = None
