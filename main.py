from fastapi import FastAPI

from config import auth_config, db_config
from routers.user import app as user_router

app = FastAPI()

app.include_router(user_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
