from fastapi import FastAPI, Path
import json
app = FastAPI()

# read the contents of the db.json file - fake db
with open("db.json") as f:
    db = json.load(f)


@app.get("/")
async def read_root():
    return {"message": "Hello World", "version": "1.0"}

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1, le=1000)
):
    return {"item_id": item_id}

@app.get("/items")
async def get_items(skip: int = 0, limit: int = 5):
    """
    Returns paginated items.
    - skip: Number of items to skip (offset)
    - limit: Maximum items to return
    """
    query = db[skip:skip+limit]
    return {"items": query}

@app.get("/search/")
def search_items(q: str | None = None) -> dict:
    if q:
        for item in db:
            if item["name"].lower() == q.lower():
                return item
        return {"error": "Item not found"}

    return {
            "items": db,
            "message": "No search query provided"
            }

