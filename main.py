from fastapi import FastAPI, Path
import json
from pydantic import BaseModel


app = FastAPI()


# define a pydantic model for the db
class Item(BaseModel):
    id: int | None = None
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

# read the contents of the db.json file - fake db
with open("db.json") as f:
    db = json.load(f)

# convert the db to a list of pydantic models
db = [Item(**item) for item in db]

print(db)
@app.get("/")
async def read_root():
    return {"message": "Hello World", "version": "2.0"}


# Use the pydantic model to validate the request body
@app.post("/items/")
async def create_item(item: Item):
    # check if the item already exists in the db
    if item.name in [item.name for item in db]:
        return {"message": "Item already exists"}
    # add the item to the db
    item.id = len(db) + 1
    db.append(item)
    return {"message": "Item added to db"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict:
    item = next((item for item in db if item.id == item_id), None)
    if item is None:
        return {"message": "Item not found"}
    tax_rate = getattr(item, 'tax', 0) or 0
    price_with_tax = item.price * (1 + tax_rate)
    return {
        "message": "Item found",
        "id": item.id,
        "name": item.name,
        "price": price_with_tax,
        "description": getattr(item, 'description', None),
        "tax": tax_rate,
    }

