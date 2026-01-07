# Day 15: Update & Delete Operations — Walkthrough

## 🎯 Goal

Complete the CRUD (Create, Read, Update, Delete) lifecycle by implementing **Partial Updates (PATCH)** and **Deletion** endpoints.

---

## ✅ What Was Implemented

### 1. Partial Update (PATCH)

We implemented a `PATCH` endpoint to allow updating specific fields of an item without requiring the entire object.

#### [main.py](file:///home/tom/projects/my-fastapi-app/main.py)

```python
@app.patch("/items/{item_id}", response_model=ItemResponse)
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
```

**Key Highlights:**
- **`exclude_unset=True`**: This is critical for `PATCH`. It ensures that only fields explicitly sent in the request body are updated.
- **`setattr`**: Dynamically updates the SQLAlchemy model instance.

---

### 2. Delete Operation

We implemented a `DELETE` endpoint to remove items from the database by their ID.

#### [main.py](file:///home/tom/projects/my-fastapi-app/main.py)

```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}
```

---

### 3. New Pydantic Model for Updates

To support partial updates, we added an `ItemUpdate` model with all fields marked as optional.

#### [models.py](file:///home/tom/projects/my-fastapi-app/models.py)

```python
class ItemUpdate(BaseModel):
    """Pydantic model for receiving partial item data via PATCH."""
    name: str | None = None
    price: float | None = None
    description: str | None = None
    tax: float | None = None
```

---

## 🧪 Verification Results

We verified the full lifecycle of an item (Create -> Update -> Read -> Delete -> Verify Deletion) using a dedicated test script.

### Automated Tests Execution

```bash
$ uv run pytest test_day_15.py
======================== 3 passed, 3 warnings in 1.14s =========================
```

**Test Cases Covered:**
1. **`test_crud_lifecycle`**:
   - Creates an item.
   - Updates only the `price` using `PATCH`.
   - Verifies the `price` changed but `name` remained the same.
   - Deletes the item.
   - Verifies a `GET` request for that ID now returns `404 Not Found`.
2. **`test_patch_non_existent`**: Verifies `404` error when patching a missing ID.
3. **`test_delete_non_existent`**: Verifies `404` error when deleting a missing ID.

---

## 📂 Files Changed

| File | Action |
|------|--------|
| [main.py](file:///home/tom/projects/my-fastapi-app/main.py) | **MODIFIED** — Added `PATCH` and `DELETE` endpoints |
| [models.py](file:///home/tom/projects/my-fastapi-app/models.py) | **MODIFIED** — Added `ItemUpdate` schema |
| [test_day_15.py](file:///home/tom/projects/my-fastapi-app/test_day_15.py) | **NEW** — Comprehensive CRUD lifecycle tests |

---

## 🔮 What's Next?

With full CRUD operations implemented, the application can now manage its state entirely through the API. Potential next steps include:
- Adding **Pagination** to the list endpoint.
- Implementing **Authentication** and **Authorization**.
- Handling **Relationships** (e.g., Categories for Items).
