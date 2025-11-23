from fastapi import FastAPI

from config import auth_config, db_config

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
