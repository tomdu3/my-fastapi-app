from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World", "version": "1.0"}

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1, le=1000)
):
    return {"item_id": item_id}

