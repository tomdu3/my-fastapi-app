from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World", "version": "1.0"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {
            "item_id": item_id,
            "message": f"Fetching item {item_id}"
            }

