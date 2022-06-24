from .entities.State import State
from .entities.Historial import Historial
from .entities.User import User
from models.ModelUser import ModelUser
from datetime import datetime
class ModelState():  
    @classmethod 
    def estadoActual(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID_HISTORIAL,ID_USUARIO,RESPONSABLE,HORA_INICIO,ID_ESTADO 
            FROM HISTORIAL WHERE ID_USUARIO={} AND TEMP_BOOLEAN=1 """.format(user.id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:  
                user=ModelUser.get_by_id(db,int(row[1]))
                historial = Historial(row[0],user.__dict__,row[2],row[3].strftime('%Y-%m-%d %H:%M:%S'),None,row[4])
                return historial
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod      
    def listState(self,db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM estados where NOMBRE_ESTADO<>'Log off' and NOMBRE_ESTADO <> 'New-hire' order by NOMBRE_ESTADO LIMIT 100;"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod       
    def call_procedure(self,db,user1,user2,estado):  
        if user2==None:
            user2=user1      
        try:
            
            today = datetime.now() 
            cursor = db.connection.cursor()
            cursor.callproc('UPDATEHISTORIAL', (user1.id,user2.nombres,today,estado))
            results = list(cursor.fetchall())
            
            return results
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod       
    def get_by_name(self,db,nombre):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_ESTADO,NOMBRE_ESTADO FROM estados WHERE NOMBRE_ESTADO = '{}'".format(nombre)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                estado=State(row[0],row[1])       
                return estado
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod       
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_ESTADO,NOMBRE_ESTADO FROM estados WHERE ID_ESTADO = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                estado=State(row[0],row[1])
                return estado
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod 
    def totalStates(self, db, user):
        try:
            lHistor=[]
            estados=[]
            
            cursor = db.connection.cursor()
            sql = """SELECT ID_HISTORIAL,ID_USUARIO,RESPONSABLE,HORA_INICIO,HORA_FINAL,ID_ESTADO FROM historial where HORA_INICIO like '%2022-06-23%' and HORA_FINAL <> 'null' order by id_estado  """.format(user.id)
            cursor.execute(sql)
            estados=list(cursor.fetchall())
            for estado in estados :
                #user=ModelUser.get_by_id(db,int(estado[1]))
                h=Historial(estado[0],estado[1],estado[2],estado[3],estado[4],estado[5],estado[4]-estado[3])
                lHistor.append(h)
            temp=lHistor[0].id_estado
            dic={}
            estado=self.get_by_id(db,lHistor[0].id_estado)
            suma=datetime.strptime("00:00:00","%H:%M:%S")
            for hist in lHistor:
                idAct=hist.id_estado
                if temp!=idAct:
                    dic[estado.nombre]=suma
                    temp=idAct
                    estado=self.get_by_id(db,idAct)
                    suma=suma=datetime.strptime("00:00:00","%H:%M:%S") 
                else:
                    #print(datetime.strptime(hist.totaltime,"%H:%M:%S"))
                    #suma = suma + datetime.strptime(hist.totaltime,"%H:%M:%S") 
                
            return dic
            #id,user,responsable,HORA_INICIO,HORA_FINAL=None,id_estado="",totaltime=""
        except Exception as ex:
            raise Exception(ex)