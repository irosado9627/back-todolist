from fastapi import APIRouter, Depends, Response
from typing import List

from src.tasks.controllers import taskController
from src.tasks.models import taskModel
from models.genericsModel import genericResponse

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[taskModel.Task])
async def get_all_tasks():
    return taskController.getAllTaks()

@router.get("/{taskID}", response_model=taskModel.Task)
def get_task_by_id(taskID: int):
    return taskController.getTaskByID(taskID)

@router.get("/username/{username}", response_model=List[taskModel.Task])
def get_task_by_username(username: str):
    return taskController.getTasksByUserName(username)

@router.post("/", response_model=genericResponse)
def create_task(task: taskModel.Task, response: Response):
    print(task)
    return taskController.createTask(task, response)

@router.put("/{taskID}", response_model=genericResponse)
def finalizar_tarea(taskID: int, response: Response):
    return taskController.finalizarTarea(taskID, response)

@router.delete("/{taskID}", response_model=genericResponse)
def delete_task(taskID: int, response: Response):
    return taskController.deleteTask(taskID, response)