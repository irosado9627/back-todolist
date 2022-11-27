import datetime
from models.db import connection
from helpers import helpers
import pymysql


def getUsers():
    with connection.cursor() as cursor:
        sql = "SELECT UserID, UserName,Estatus,FechaAlta,FechaBaja,FechaBloq FROM USERS WHERE Estatus = %s"
        cursor.execute(sql, ('A',))
        result = cursor.fetchall()
        print(result)
        return result


def create_user(user):
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
        connection.commit()
        cursor.close()
        return createdUser

def user_activate(username):
    return changeStatusUser(username, 'A')

def deleteUser(username):
    return changeStatusUser(username, 'C')

def bloquearUser(username):
    return changeStatusUser(username, 'B')

def changeStatusUser(username: str, action: str):
    with connection.cursor() as cursor:
        activateddUser ={}
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
        except Exception as ex:
            connection.rollback()
            print('Ocurrió un error al intentar actualizar el usuario', ex)
            activateddUser = {
                "msg": "Ocurrió un error al intentar actualizar el usuario",
                "UserName": ""
            }
        connection.commit()
        cursor.close()
        return activateddUser