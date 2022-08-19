from ast import Try
from logging import exception
from .entities.User import User
from werkzeug.security import generate_password_hash
class ModelUser():

    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID_USUARIO, CORREO_SOLVO, ID_COMPANIA, ID_CIUDAD, CONTRASENA, ID_SOLVO, NOMBRES, APELLIDOS, ESTADO, PERFIL, ID_SUPERVISOR FROM usuario 
                    WHERE CORREO_SOLVO = '{}'""".format(user.correo_solvo)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                # compCiu=ModelUser.getCompCiu(db,row[9])
                user = User(row[0], row[1],row[2],row[3], User.check_password(row[4], user.contrasena), row[5],row[6],row[7],row[8],row[9],row[10])
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
                user = User(0,row[0],None,None)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def addAdmin(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO USUARIO (ID_USUARIO,CORREO_SOLVO,ID_COMPANIA,ID_CIUDAD,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,PERFIL,ESTADO)
                VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql,(user.correo_solvo,user.compania,user.ciudad,generate_password_hash(user.contrasena),user.id_solvo,user.nombres,user.apellidos,user.perfil,user.estado))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def addSup(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO USUARIO (ID_USUARIO,CORREO_SOLVO,ID_COMPANIA,ID_CIUDAD,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,PERFIL,ESTADO,ID_SUPERVISOR)
                VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql,(user.correo_solvo,user.compania,user.ciudad,generate_password_hash(user.contrasena),user.id_solvo,user.nombres,user.apellidos,user.perfil,user.estado,user.id_supervisor))
            db.connection.commit() 
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, CORREO_SOLVO, ID_COMPANIA, ID_CIUDAD, ID_SOLVO, NOMBRES, APELLIDOS, ESTADO, PERFIL, ID_SUPERVISOR FROM usuario WHERE ID_USUARIO = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                # compCiu=ModelUser.getCompCiu(db,row[8])
                Usuario=User(row[0], row[1],row[2],row[3],None, row[4],row[5],row[6],row[7],row[8],row[9])
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
            sql = "SELECT ID_USUARIO, NOMBRES, APELLIDOS FROM usuario WHERE PERFIL = 1 and ESTADO = 'ACTIVO'"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ListSup(self,db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, NOMBRES, APELLIDOS FROM usuario WHERE PERFIL = 2 and ESTADO = 'ACTIVO'"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ListTeam(self,db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_USUARIO, NOMBRES, APELLIDOS FROM usuario WHERE PERFIL = 3 and ESTADO = 'ACTIVO'"
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
            sql = "SELECT ID_USUARIO, ID_SOLVO, NOMBRES, APELLIDOS, CORREO_SOLVO, ID_SUPERVISOR, ID_COMPANIA, ID_CIUDAD, PERFIL FROM usuario WHERE ID_USUARIO={}".format(id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def UpdateAdmin(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuario SET ID_SOLVO=%s, NOMBRES=%s, APELLIDOS=%s, CORREO_SOLVO=%s, ID_COMPANIA=%s, ID_CIUDAD=%s, PERFIL=%s WHERE ID_USUARIO=%s"
            cursor.execute(sql,(user.id_solvo,user.nombres,user.apellidos,user.correo_solvo,user.compania,user.ciudad,user.perfil,user.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def UpdateSup(self, db, user):
        try:
            # print(user.__dic__)
            # CC=ModelUser.Co_ci_CC(db,None,None)
            cursor = db.connection.cursor()
            sql = "UPDATE usuario SET ID_SOLVO=%s, NOMBRES=%s, APELLIDOS=%s, CORREO_SOLVO=%s, ID_SUPERVISOR=%s, ID_COMPANIA=%s, ID_CIUDAD=%s, PERFIL=%s WHERE ID_USUARIO=%s"
            cursor.execute(sql,(user.id_solvo,user.nombres,user.apellidos,user.correo_solvo,user.id_supervisor,user.compania,user.ciudad,user.perfil,user.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
            
    # @classmethod
    # def Co_ci_CC(self,db,idCo,idCi):
    #     try:
    #         cursor = db.connection.cursor()
    #         sql = "Select ID_COMCIU from companiaciudad where ID_COMPANIA=%s and ID_CIUDAD=%s"
    #         cursor.execute(sql,(1,1))
    #         id = cursor.fetchone()
    #         return id
    #     except Exception as ex:
    #         raise Exception(ex)
        
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
    def listCity(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_CIUDAD, NOMBRE_CIUDAD from ciudad"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def listCompany(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_COMPANIA, NOMBRE_COMPANIA from compania"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getCompCiu(self,db,idCC):
        try:
            compCiu={}
            cursor = db.connection.cursor()
            sql = """select  com.id_compania,com.NOMBRE_COMPANIA,ciu.id_ciudad,ciu.nombre_ciudad 
                        from companiaciudad as CC
                        inner join compania as com on CC.ID_COMPANIA = com.id_compania 
                        inner join ciudad as ciu on CC.ID_CIUDAD=ciu.id_ciudad
                        where CC.ID_COMCIU={}""".format(idCC)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                compCiu['compania']={'id':row[0],'nombre':row[1]}
                compCiu['ciudad']={'id':row[2],'nombre':row[3]}
                return compCiu
            else:
                return compCiu
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getCompCiuTodos(self,db):
        try:
            lista=[]
            cursor = db.connection.cursor()
            sql = """select CC.ID_COMCIU, com.id_compania, com.NOMBRE_COMPANIA, ciu.id_ciudad, ciu.nombre_ciudad 
                        from companiaciudad as CC
                        inner join compania as com on CC.ID_COMPANIA = com.id_compania 
                        inner join ciudad as ciu on CC.ID_CIUDAD=ciu.id_ciudad"""
            cursor.execute(sql)
            compCiu=list(cursor.fetchall())
            for row in compCiu :
                lista.append({'id':row[0],'compania':{'id':row[1],'nombre':row[2]},'ciudad':{'id':row[3],'nombre':row[4]}})
            return lista
        except Exception as ex:
            raise Exception(ex)
