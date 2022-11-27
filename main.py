from typing import Union

from fastapi import FastAPI

from src.users.routers import userRouter

app = FastAPI()

app.include_router(userRouter.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}