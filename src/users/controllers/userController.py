from src.users.services import usersService

def getUsers():
    return usersService.getUsers()

def create_user(User, response):
    return usersService.create_user(User)

def user_activate(username: str,response):
    return usersService.user_activate(username,response)

def deleteUser(username: str,response):
    return usersService.deleteUser(username,response)

def bloquearUser(username: str,response):
    return usersService.bloquearUser(username,response)

def getUserByUserName(username: str):
    return usersService.getUserByUserName(username)

def change_password(username: str, pw: str, response):
    return usersService.change_password(username, pw, response)