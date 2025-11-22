from fastapi import FastAPI

from config import authconfig, db_config

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
