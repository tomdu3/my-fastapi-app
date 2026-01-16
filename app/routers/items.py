from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
import app.models as models
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemPublic
from app.dependencies import get_current_user
from app.schemas.user import User

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
    query = db.query(models.ItemDB)
    if q:
        query = query.filter(models.ItemDB.name.contains(q))
    
    results = query.all()
    if not results:
        return []
    return results


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # 1. Create the DB object
    db_item = models.ItemDB(**item.dict())
    # 2. Add and Commit
    db.add(db_item)
    db.commit()
    # 3. Refresh to get the generated ID
    db.refresh(db_item)
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
    item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    # 1. Find the item
    db_item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # 2. Update only the fields provided
    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    # 3. Save and return
    db.commit()
    db.refresh(db_item)
    return {"message": "Item updated", "item": db_item}


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}
