from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.users.controllers import userController
from src.users.models import userModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[userModel.User])
async def read_items():
    return userController.getUsers()

@router.post("/", response_model=userModel.UserCreated)
def create_user(user: userModel.User):
    return userController.create_user(user)

@router.put("/activar/{username}")
def user_activate(username: str):
    return userController.user_activate(username)

@router.delete("/{username}")
def deleteUser(username: str):
    return userController.deleteUser(username)

@router.put("/bloquear/{username}")
def bloquearUser(username: str):
    return userController.bloquearUser(username)