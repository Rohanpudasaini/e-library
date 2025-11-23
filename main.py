from fastapi import FastAPI

from routers.book import app as book_router
from routers.user import app as user_router

app = FastAPI()

app.include_router(book_router, tags=["Book"])
app.include_router(user_router, tags=["User"])


@app.get("/")
async def read_root():
    return {"Hello": "World"}
