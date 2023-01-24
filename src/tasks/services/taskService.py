import datetime
from models.db import connection
import pymysql
from fastapi import Response

def getAllTaks():
    with connection.cursor() as cursor:
        sql = "SELECT t.TaskID, t.UserID, u.UserName, t.Titulo, t.Descripcion, t.CreadoEn, t.FinalizadoEn, t.Finalizado FROM TASKS t INNER JOIN USERS u ON t.UserID = u.UserID"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        connection.commit()
        return result

def getTaskByID(taskID: int):
    with connection.cursor() as cursor:
        sql = "SELECT t.TaskID, t.UserID, u.UserName, t.Titulo, t.Descripcion, t.CreadoEn, t.FinalizadoEn, t.Finalizado FROM TASKS t INNER JOIN USERS u ON t.UserID = u.UserID WHERE t.TaskID = %s"
        cursor.execute(sql, (taskID,))
        result = cursor.fetchone()
        print(result)
        connection.commit()
        return result

def getTasksByUserName(username: str):
    with connection.cursor() as cursor:
        sql = "SELECT t.TaskID, t.UserID, u.UserName, t.Titulo, t.Descripcion, t.CreadoEn, t.FinalizadoEn, t.Finalizado FROM TASKS t INNER JOIN USERS u ON t.UserID = u.UserID WHERE u.username = %s"
        cursor.execute(sql, (username.lower(),))
        result = cursor.fetchall()
        print(result)
        connection.commit()
        return result

def createTask(task, response: Response):
    print(task)
    with connection.cursor() as cursor:
        createdUser ={}
        try:
            sql2 = "SELECT ifnull(MAX(TaskID),0) as id FROM TASKS"
            cursor.execute(sql2)
            taskID = cursor.fetchone()
            taskID = taskID["id"] + 1

            sql = "INSERT INTO TASKS(TaskID, UserID, Titulo, Descripcion, CreadoEn) VALUES (%s, %s, %s, %s, %s)"
            fechaActual = datetime.datetime.now()
            AudFecha = fechaActual.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(sql, (taskID, task.UserID, task.Titulo,task.Descripcion,AudFecha,))
        
            createdUser = {
                "msg": "Tarea creada de manera exitosa",
                "data": {
                    "taskID": taskID
                }
            }

        except pymysql.err.IntegrityError as e:
            print("Error: {}".format(e))
            connection.rollback()
            response.status_code = 400
            createdUser = {
                "msg": "Error: {}".format(e),
                "data": {
                    "taskID": 0
                }
            }
        except Exception as ex:
            connection.rollback()
            print('Ocurrió un error al intentar crear la tarea', ex)
            createdUser = {
                "msg": "Ocurrió un error al intentar crear la tarea",
                "data": {
                    "taskID": 0
                }
            }
            response.status_code = 500
        connection.commit()
        cursor.close()
        return createdUser

def finalizarTarea(taskID: int, response: Response):
    with connection.cursor() as cursor:
        sql2 = "SELECT ifnull(Finalizado,0) as finalizado FROM TASKS where TaskID = %s"
        cursor.execute(sql2, (taskID,))

        res = cursor.fetchone()
        tareaFinalizada ={}
        if res is None:
            response.status_code = 404
            tareaFinalizada = {
            "msg": "No se encontró una tarea con el id {}".format(taskID),
            "data": {
                    "taskID": taskID
                }
            }
        else:
            if res['finalizado'] == 1:
                response.status_code = 400
                tareaFinalizada = {
                "msg": "La tarea con el id {} ya fue finalizada con anterioridad".format(taskID),
                "data": {
                    "taskID": taskID
                }
                }
            else:
                fechaActual = datetime.datetime.now()
                AudFecha = fechaActual.strftime("%Y-%m-%d %H:%M:%S")

                try:
                    sql = "UPDATE TASKS SET Finalizado = 1, FinalizadoEn = %s WHERE TaskID = %s"
                    print(sql, (taskID,))
                    cursor.execute(sql, (AudFecha, taskID,))
                    tareaFinalizada = {
                        "msg": "Tarea Finalizada de manera correcta",
                        "data": {
                            "taskID": taskID
                        }
                    }
                except pymysql.err.IntegrityError as e:
                    print("Error: {}".format(e))
                    connection.rollback()
                    tareaFinalizada = {
                        "msg": "Error: {}".format(e),
                        "data": {
                            "taskID": 0
                        }
                    }
                    response.status_code = 400
                except Exception as ex:
                    connection.rollback()
                    print('Ocurrió un error al intentar finalizar la tarea', ex)
                    tareaFinalizada = {
                        "msg": "Ocurrió un error al intentar finalizar la tarea",
                        "data": {
                            "taskID": 0
                        }
                    }
                    response.status_code = 500
        connection.commit()
        cursor.close()
        return tareaFinalizada

def deleteTask(taskID: int, response: Response):
    with connection.cursor() as cursor:
        sql2 = "SELECT ifnull(Finalizado,0) as finalizado FROM TASKS where TaskID = %s"
        cursor.execute(sql2, (taskID,))

        res = cursor.fetchone()
        tareaFinalizada ={}
        if res is None:
            response.status_code = 404
            tareaFinalizada = {
            "msg": "No se encontró una tarea con el id {}".format(taskID),
            "data": {
                    "taskID": taskID
                }
            }
        else:
            try:
                sql = "DELETE FROM TASKS WHERE TaskID = %s"
                print(sql, (taskID,))
                cursor.execute(sql,(taskID,))
                tareaFinalizada = {
                    "msg": "Tarea eliminada de manera correcta",
                    "data": {
                        "taskID": taskID
                    }
                }
            except pymysql.err.IntegrityError as e:
                print("Error: {}".format(e))
                connection.rollback()
                tareaFinalizada = {
                    "msg": "Error: {}".format(e),
                    "data": {
                        "taskID": 0
                    }
                }
                response.status_code = 400
            except Exception as ex:
                connection.rollback()
                print('Ocurrió un error al intentar eliminar la tarea', ex)
                tareaFinalizada = {
                    "msg": "Ocurrió un error al intentar eliminar la tarea",
                    "data": {
                        "taskID": 0
                    }
                }
                response.status_code = 500
        connection.commit()
        cursor.close()
        return tareaFinalizada