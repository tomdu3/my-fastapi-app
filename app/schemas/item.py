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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Quantum Processor",
                    "price": 999.99,
                    "description": "A very fast CPU.",
                    "tax": 80.0
                }
            ]
        }
    }


class ItemUpdate(BaseModel):
    """Pydantic model for receiving partial item data via PATCH."""
    name: str | None = None
    price: float | None = None
    description: str | None = None
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "price": 899.99,
                    "description": "Updated fast CPU."
                }
            ]
        }
    }


class ItemPublic(BaseModel):
    """Pydantic model for public API responses (hides internal fields)."""
    name: str
    price: float
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Quantum Processor",
                    "price": 999.99,
                    "description": "A very fast CPU."
                }
            ]
        }
    }


class ItemResponse(BaseModel):
    """Pydantic model for structured API responses with message."""
    message: str
    item: ItemPublic | None = None
