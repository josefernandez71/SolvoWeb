from .entities.User import User
from werkzeug.security import check_password_hash,generate_password_hash
class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID_INTERPRETER,CORREO_SOLVO,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,ESTADO,ID_SUPERVISOR FROM interpreter 
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
    def ExistsUser(self, db, user,tipo):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT CORREO_SOLVO FROM interpreter 
                    WHERE CORREO_SOLVO = '{}'""".format(user.correo_solvo)        
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(0,row[0],"")
                print(str(user))
                return user
            else:
                sql = """SELECT CORREO_SOLVO FROM supervisor 
                    WHERE CORREO_SOLVO = '{}'""".format(user.correo_solvo)        
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    user = User(0,row[0],"")
                    print(str(user))
                    return user
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def addInterp(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO interpreter (ID_INTERPRETER,CORREO_SOLVO,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,ESTADO,ID_SUPERVISOR)
                VALUES (null,%s,%s, %s, %s,%s,%s,%s)"""
            cursor.execute(sql,(user.correo_solvo,generate_password_hash(user.contrasena),user.id_solvo,user.nombres,user.apellidos,user.estado,user.id_supervisor))
            db.connection.commit()   
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def addSup(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO supervisor (ID_SUPERVISOR,CORREO_SOLVO,CONTRASENA,ID_SOLVO,NOMBRES,APELLIDOS,ESTADO)
                VALUES (null,%s,%s, %s,%s,%s,%s)"""
            cursor.execute(sql,(user.correo_solvo,generate_password_hash(user.contrasena),user.id_solvo,user.nombres,user.apellidos,user.estado))
            db.connection.commit()   
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_INTERPRETER,CORREO_SOLVO,ID_SOLVO,NOMBRES,APELLIDOS,ESTADO,ID_SUPERVISOR FROM interpreter WHERE ID_INTERPRETER = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                Usuario=User(row[0], row[1], None, row[2],row[3],row[4],row[5],row[6])
                #print(str(Usuario))
                return Usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)