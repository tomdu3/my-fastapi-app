from fastapi import (
    FastAPI,
    Path,
    Query,
    HTTPException,
    Request,
    Depends,
    Form,
    File,
    UploadFile,
)

from typing import Annotated
from fastapi.responses import JSONResponse
from starlette.exceptions import (
    HTTPException as StarletteHTTPException
)
from datetime import datetime
import json
from pydantic import BaseModel


app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": request.url.path,
            "code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        },
    )


# define a pydantic model for the db
class Item(BaseModel):
    id: int | None = None
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

# define a pydantic model for the response
class ItemPublic(BaseModel):
    name: str
    price: float
    description: str | None = None

class ItemResponse(BaseModel):
    message: str
    item: ItemPublic | None = None

# read the contents of the db.json file - fake db
with open("db.json") as f:
    db = json.load(f)

# convert the db to a list of pydantic models
db = [Item(**item) for item in db]

# Define the database dependency
def get_db():
    # In a real app, this is where you'd open a DB session
    return db


@app.get("/")
async def read_root():
    return {"message": "Hello World", "version": "2.0"}


@app.get("/items/")
async def read_items(
    database: Annotated[list, Depends(get_db)],
    q: str | None = Query(
        None,
        min_length=3,
        max_length=50,
        title="Search Query",
        description="Search for items in the database",
    )  # use Query to validate the query parameter - min_length and max_length are the minimum and maximum length of the query parameter
):
    results = [
        item for item in database if q.lower() in item.name.lower()
        ] if q else database
    if not results:
        return {"message": "No items found"}
    return results


@app.post("/items/", status_code=201)
async def create_item(item: Item, database: Annotated[list, Depends(get_db)]):
    # check if the item already exists in the db
    if item.name in [db_item.name for db_item in database]:
        raise HTTPException(status_code=400, detail="Item already exists")
    # add the item to the db
    item.id = len(database) + 1
    database.append(item)
    return {"message": "Item added to db"}

# returns a pydantic model for the response
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(
    database: Annotated[list, Depends(get_db)],
    item_id: int = Path(..., title="The ID of the item", gt=0, le=1000)
) -> ItemResponse:  # use Path to validate the path parameter- gt and le are greater than and less than

    item = next((db_item for db_item in database if db_item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    tax_rate = getattr(item, 'tax', 0) or 0
    price_with_tax = item.price * (1 + tax_rate)
    message = "Item found"
    return ItemResponse(
        message=message,
        item=ItemPublic(
            name=item.name,
            price=price_with_tax,
            description=item.description,
        )
    )


# Form Data and File Uploads
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    """Handle form-based login (not JSON)"""
    return {"username": username}


@app.post("/upload-profile-pic/")
async def upload_image(file: UploadFile = File(...)):
    """Upload a file using UploadFile for memory-efficient handling"""
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }


@app.post("/upload-with-description/")
async def upload_with_description(
    description: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload a file along with form field data (multipart request)"""
    contents = await file.read()
    return {
        "description": description,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }
