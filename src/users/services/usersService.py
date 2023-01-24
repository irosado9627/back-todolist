import datetime
from models.db import connection
from helpers import helpers
import pymysql
import bcrypt
from fastapi import Response

def getUsers():
    with connection.cursor() as cursor:
        sql = "SELECT UserID, UserName,Estatus,FechaAlta,FechaBaja,FechaBloq FROM USERS WHERE Estatus = %s"
        cursor.execute(sql, ('A',))
        result = cursor.fetchall()
        print(result)
        connection.commit()
        return result

def getUserByUserName(username):
    with connection.cursor() as cursor:
        sql = "SELECT UserID, UserName,Estatus,FechaAlta,FechaBaja,FechaBloq FROM USERS WHERE UserName LIKE %s AND Estatus = %s"
        cursor.execute(sql, ("%" + username + "%", 'A',))
        result = cursor.fetchall()
        print(result)
        connection.commit()
        return result

def create_user(user, response: Response):
    with connection.cursor() as cursor:
        createdUser ={}
        try:
            sql2 = "SELECT ifnull(MAX(UserID),0) as id FROM USERS"
            cursor.execute(sql2)
            userID = cursor.fetchone()
            userID = userID["id"] + 1

            sql = "INSERT INTO USERS(UserID, UserName, Password, FechaAlta, AudFecha) VALUES(%s, %s, %s, %s, %s);"
            fechaActual = datetime.datetime.now()
            AudFecha = fechaActual.strftime("%Y-%m-%d %H:%M:%S")
            fechaAlta = fechaActual.strftime("%Y-%m-%d")
            pw = helpers.hasPass(user.Password.encode('utf-8'))
            
            cursor.execute(sql, (userID, user.UserName.lower(), pw,fechaAlta,AudFecha))
        
            createdUser = {
                "msg": "Usuario creado de manera exitosa",
                "UserName": user.UserName
            }
        except pymysql.err.IntegrityError as e:
            print("Error: {}".format(e))
            connection.rollback()
            response.status_code = 400
            createdUser = {
                "msg": "Error: {}".format(e),
                "UserName": ""
            }
        except Exception as ex:
            connection.rollback()
            print('Ocurrió un error al intentar crear el usuario', ex)
            createdUser = {
                "msg": "Ocurrió un error al intentar crear el usuario",
                "UserName": ""
            }
            response.status_code = 500
        connection.commit()
        cursor.close()
        return createdUser

def user_activate(username,response):
    return changeStatusUser(username, 'A',response)

def deleteUser(username,response):
    return changeStatusUser(username, 'C',response)

def bloquearUser(username,response):
    return changeStatusUser(username, 'B',response)

def change_password(username: str, password: str, response: Response):
    with connection.cursor() as cursor:
        createdUser ={}
        try:
            sql = "SELECT IFNULL(Password,'') as pw FROM USERS where UserName = %s"
            cursor.execute(sql, (username,))

            res = cursor.fetchone()
            if res is None:
                response.status_code = 404
                createdUser = {
                "msg": "No se encontró un usuario con el username",
                "UserName": username
                }
            else:
                print(res)
                pwActual = res["pw"]
                if bcrypt.checkpw(password.encode('utf-8'), pwActual.encode('utf-8')):
                    createdUser = {
                    "msg": "La nueva contraseña no debe ser la misma que la contraseña actual",
                    "UserName": username
                    }
                    response.status_code = 400
                else:
                    createdUser = {
                        "msg": "La contraseña fue actualizada de manera exitosa",
                        "UserName": username
                    }
        
        except Exception as ex:
            connection.rollback()
            print('Ocurrió un error al intentar actualizar la contraseña del usuario {}'.format(username), ex)
            createdUser = {
                "msg": "Ocurrió un error al intentar actualizar la contraseña del usuario {}".format(username),
                "UserName": username
            }
        connection.commit()
        cursor.close()
        return createdUser

def changeStatusUser(username: str, action: str, response: Response):
    with connection.cursor() as cursor:
        sql2 = "SELECT IFNULL(Password,'') as pw, ifnull(UserID,0) as UserID FROM USERS where UserName = %s"
        cursor.execute(sql2, (username,))

        res = cursor.fetchone()
        activateddUser ={}
        if res is None:
            response.status_code = 404
            activateddUser = {
            "msg": "No se encontró un usuario con el username",
            "UserName": username
            }
        else:
            
            fechaActual = datetime.datetime.now()
            AudFecha = fechaActual.strftime("%Y-%m-%d %H:%M:%S")

            acc = ''
            camposAdici = ''
            if action == 'A':
                acc = 'activado'
                camposAdici = ", FechaBaja = null, FechaBloq = null"
            elif action == 'C':
                acc = 'ha sido dado de baja' 
                camposAdici = ", FechaBaja = '"+ AudFecha + "'"
            elif action == 'B':
                acc = 'Bloqueado'
                camposAdici = ", FechaBloq = '"+ AudFecha + "'"
            else:
                acc = 'inactivado'
            #"," + camposAdici + "'"+ fechaActual.strftime("%Y-%m-%d")+ "'"
            try:
                sql = "UPDATE USERS SET Estatus = %s {} WHERE UserName = %s".format(camposAdici) 
                print(sql, (action, username,))
                cursor.execute(sql, (action, username,))
                activateddUser = {
                    "msg": "Usuario {} de manera correcta".format(acc),
                    "UserName": username
                }
            except pymysql.err.IntegrityError as e:
                print("Error: {}".format(e))
                connection.rollback()
                activateddUser = {
                    "msg": "Error: {}".format(e),
                    "UserName": ""
                }
                response.status_code = 400
            except Exception as ex:
                connection.rollback()
                print('Ocurrió un error al intentar actualizar el usuario', ex)
                activateddUser = {
                    "msg": "Ocurrió un error al intentar actualizar el usuario",
                    "UserName": ""
                }
                response.status_code = 500
        connection.commit()
        cursor.close()
        return activateddUser