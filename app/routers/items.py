from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
import app.models as models
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemPublic
from app.dependencies import get_current_user
from app.schemas.user import User

from app.repositories import ItemRepository

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

@router.get("/", response_model=list[ItemPublic])
async def read_items(
    db: Annotated[Session, Depends(get_db)],
    q: str | None = Query(
        None,
        min_length=3,
        max_length=50,
        title="Search Query",
        description="Search for items in the database",
    )
):
    repo = ItemRepository(db)
    return repo.search(q)


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    repo = ItemRepository(db)
    db_item = repo.create(item.dict())
    return {"message": "Item created", "item": db_item}


@router.get("/secret")
async def read_secret_items(current_user: Annotated[User, Depends(get_current_user)]):
    """
    A protected route that requires a valid JWT token.
    Validation is handled by the get_current_user dependency.
    """
    return {
        "message": f"Hello {current_user.username}! This is a protected route.",
        "user_details": current_user
    }


@router.get("/{item_id}", response_model=ItemPublic)
def read_item(item_id: int, db: Session = Depends(get_db)):
    repo = ItemRepository(db)
    item = repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    repo = ItemRepository(db)
    db_item = repo.get_by_id(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only the fields provided
    update_data = item_update.dict(exclude_unset=True)
    repo.update(db_item, update_data)
    
    return {"message": "Item updated", "item": db_item}


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    repo = ItemRepository(db)
    if not repo.delete(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
