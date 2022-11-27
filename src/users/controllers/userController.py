from src.users.services import usersService

def getUsers():
    return usersService.getUsers()

def create_user(User):
    return usersService.create_user(User)

def user_activate(username: str):
    return usersService.user_activate(username)

def deleteUser(username: str):
    return usersService.deleteUser(username)

def bloquearUser(username: str):
    return usersService.bloquearUser(username)