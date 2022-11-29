from fastapi import APIRouter, Depends, Response
from typing import List

from src.users.controllers import userController
from src.users.models import userModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[userModel.User])
async def getUsers():
    return userController.getUsers()

@router.get("/{username}", response_model=List[userModel.User])
async def getUserByUserName(username: str):
    return userController.getUserByUserName(username)

@router.post("/", response_model=userModel.UserCreated)
def create_user(user: userModel.User, response: Response):
    return userController.create_user(user, response)

@router.put("/activar/{username}")
def user_activate(username: str, response: Response):
    return userController.user_activate(username,response)

@router.delete("/{username}")
def deleteUser(username: str, response: Response):
    return userController.deleteUser(username,response)

@router.put("/bloquear/{username}")
def bloquearUser(username: str, response: Response):
    return userController.bloquearUser(username,response)


@router.put("/change-pw")
def change_password(username: str, pw:str, response: Response):
    return userController.change_password(username, pw,response)
