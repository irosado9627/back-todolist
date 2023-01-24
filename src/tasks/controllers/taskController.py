from src.tasks.services import taskService

def getAllTaks():
    return taskService.getAllTaks()

def getTaskByID(taskID: int):
    return taskService.getTaskByID(taskID)

def getTasksByUserName(username: str):
    return taskService.getTasksByUserName(username)

def createTask(task, response):
    return taskService.createTask(task, response)

def finalizarTarea(taskID: int, response):
    return taskService.finalizarTarea(taskID, response)

def deleteTask( taskID: int, response ):
    return taskService.deleteTask(taskID, response)