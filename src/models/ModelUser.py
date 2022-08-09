from sys import flags
from colorama import Cursor
from flask import flash
from .entities.User import User
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime
class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID_USUARIO,CORREO_SOLVO,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,ESTADO,ID_SUPERVISOR FROM usuario 
                    WHERE CORREO_SOLVO = '{}'""".format(user.correo_solvo)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.contrasena), row[3],row[4],row[5],row[6])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def ExistsUser(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT CORREO_SOLVO FROM usuario 
                    WHERE CORREO_SOLVO = '{}'""".format(user.correo_solvo)        
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(0,row[0])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def addAdmin(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO USUARIO (ID_USUARIO,CORREO_SOLVO,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,ID_COMPANIACIUDAD,PERFIL,ESTADO)
                VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql,(user.correo_solvo,generate_password_hash(user.contrasena),user.id_solvo,user.nombres,user.apellidos,user.id_compciu,user.perfil,user.estado))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def addSup(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO USUARIO (ID_USUARIO,CORREO_SOLVO,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,ID_COMPANIACIUDAD,PERFIL,ESTADO,ID_SUPERVISOR)
                VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql,(user.correo_solvo,generate_password_hash(user.contrasena),user.id_solvo,user.nombres,user.apellidos,user.id_compciu,user.perfil,user.estado,user.id_supervisor))
            db.connection.commit() 
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO,CORREO_SOLVO,ID_SOLVO,NOMBRES,APELLIDOS,ESTADO,ID_SUPERVISOR FROM usuario WHERE ID_USUARIO = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                Usuario=User(row[0], row[1], None, row[2],row[3],row[4],row[5],row[6])
                return Usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def perfil(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_PERFIL, NOMBRE_PERFIL FROM perfiles"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def ListAdmin(self,db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, NOMBRES, APELLIDOS FROM usuario WHERE PERFIL = 1 "
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ListSup(self,db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, NOMBRES, APELLIDOS FROM usuario WHERE PERFIL = 2 "
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ListTeam(self,db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, NOMBRES, APELLIDOS FROM usuario WHERE PERFIL = 3 "
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def Show(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, ID_SOLVO, NOMBRES, APELLIDOS, CORREO_SOLVO, ESTADO from usuario"
            cursor.execute(sql)
            return cursor.fetchall() 
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, ID_SOLVO, NOMBRES, APELLIDOS, CORREO_SOLVO, ID_SUPERVISOR, ID_COMPANIACIUDAD, PERFIL FROM usuario WHERE ID_USUARIO={}".format(id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def UpdateAdmin(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuario SET ID_SOLVO=%s, NOMBRES=%s, APELLIDOS=%s, CORREO_SOLVO=%s, ID_COMPANIACIUDAD=%s, PERFIL=%s WHERE ID_USUARIO=%s"
            cursor.execute(sql,(user.id_solvo,user.nombres,user.apellidos,user.correo_solvo,user.id_compciu,user.perfil,user.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def UpdateSup(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuario SET ID_SOLVO=%s, NOMBRES=%s, APELLIDOS=%s, CORREO_SOLVO=%s, ID_SUPERVISOR=%s, ID_COMPANIACIUDAD=%s, PERFIL=%s WHERE ID_USUARIO=%s"
            cursor.execute(sql,(user.id_solvo,user.nombres,user.apellidos,user.correo_solvo,user.id_supervisor,user.id_compciu,user.perfil,user.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ShowUser(self, db, id):
        try: 
            cursor = db.connection.cursor()
            sql = """SELECT ID_USUARIO, ID_SOLVO, NOMBRES, APELLIDOS, CORREO_SOLVO, PERFIL, id_supervisor, ID_COMPANIACIUDAD
            FROM usuario where usuario.ID_USUARIO = {}""".format(id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def user(self, db):
        try: 
            cursor = db.connection.cursor()
            sql = """SELECT ID_USUARIO, ID_SOLVO, NOMBRES, APELLIDOS, CORREO_SOLVO, PERFIL, id_supervisor, ID_COMPANIACIUDAD
                FROM usuario"""
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def traerEstado(self, db, id):
        try: 
            cursor = db.connection.cursor()
            sql = "SELECT ESTADO FROM usuario WHERE ID_USUARIO={}".format(id)
            cursor.execute(sql)
            return cursor.fetchone()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def State(self, db, id, estado):
        state = str(estado)
        try:
            if state == "('activo',)" or state == "('ACTIVO',)":
                cursor = db.connection.cursor()
                sql  = "UPDATE usuario SET ESTADO='INACTIVO' WHERE ID_USUARIO={}".format(id)
                cursor.execute(sql)
                db.connection.commit()
            elif state == "('inactivo',)" or state == "('INACTIVO',)":
                cursor = db.connection.cursor()
                sql  = "UPDATE usuario SET ESTADO='ACTIVO' WHERE ID_USUARIO={}".format(id)
                cursor.execute(sql)
                db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def CompanyCity(self,db):
        try:
            cursor = db.connection.cursor()
            sql= """select companiaciudad.ID_COMCIU, compania.NOMBRE_COMPANIA, ciudad.NOMBRE_CIUDAD from companiaciudad 
            INNER join compania on compania.ID_COMPANIA=companiaciudad.ID_COMPANIA
            INNER JOIN ciudad on ciudad.ID_CIUDAD=companiaciudad.ID_CIUDAD"""
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
            