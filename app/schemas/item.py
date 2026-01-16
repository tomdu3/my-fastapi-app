from pydantic import BaseModel

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
