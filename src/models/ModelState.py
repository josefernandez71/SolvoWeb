from .entities.State import State
from .entities.Historial import Historial
from .entities.User import User
from models.ModelUser import ModelUser
from datetime import datetime,timezone


class ModelState():  
    @classmethod 
    def estadoActual(self,db,user):
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
            
            lestados=[]
            estados=[]
            cursor = db.connection.cursor()
            sql = "SELECT * FROM estados where NOMBRE_ESTADO<>'Log off' and NOMBRE_ESTADO <> 'New-hire' order by NOMBRE_ESTADO LIMIT 100;"
            cursor.execute(sql)
            estados=list(cursor.fetchall())
            for estado in estados :
                h=State(estado[0],estado[1])
                lestados.append(h)
            return lestados
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
    def totalStates(self,db, user):
        try:
            
            lHistor=[]
            estados=[]
            today = datetime.now() 
            cursor = db.connection.cursor()
            sql = """SELECT ID_HISTORIAL,ID_USUARIO,RESPONSABLE,HORA_INICIO,HORA_FINAL,ID_ESTADO 
                    FROM historial
                    where ID_USUARIO={} and ID_ESTADO <> 1 and HORA_INICIO like '%{}%' and HORA_FINAL <> 'null' order by id_estado  """.format(user.id,today.strftime("%Y-%m-%d"))
            cursor.execute(sql)
            estados=list(cursor.fetchall())#
            for estado in estados :
                #user=ModelUser.get_by_id(db,int(estado[1]))
                
                h=Historial(estado[0],estado[1],estado[2],estado[3].strftime('%Y-%m-%d %H:%M:%S'),estado[4].strftime('%Y-%m-%d %H:%M:%S'),estado[5],estado[4]-estado[3])
                lHistor.append(h)
            if not lHistor:
                lState=self.listState(db)
                dic={}
                for s in lState:
                    dic[s.nombre]='0'
            
                return dic
            else:
                lState=self.listState(db)
                temp=lHistor[0].id_estado
                dic={}
                for s in lState:
                    dic[s.nombre]='0'
                estado=self.get_by_id(db,lHistor[0].id_estado)
                suma=lHistor[0].totaltime
                #print(suma)
                for hist in lHistor:
                    idAct=hist.id_estado
                    if temp!=idAct:
                        dic[estado.nombre]=str(suma.seconds*1000)
                        #print(suma.seconds*1000,estado.nombre)
                        temp=idAct
                        estado=self.get_by_id(db,idAct)
                        suma=hist.totaltime
                    else:
                        suma = suma + hist.totaltime
                dic[estado.nombre]=str(suma.seconds*1000)
                
                return dic
        except Exception as ex:
            raise Exception(ex)

        
    @classmethod
    def listRTS(self,db,compania):
        try:
            lHistor=[]
            estados=[]
            today = datetime.now() 
            cursor = db.connection.cursor()
            sql = """SELECT ID_HISTORIAL,ID_USUARIO,RESPONSABLE,HORA_INICIO,ID_ESTADO 
                    FROM historial
                    where TEMP_BOOLEAN = 1 and ID_ESTADO <> 1 and ID_ESTADO <> 3  """
            cursor.execute(sql)
            estados=list(cursor.fetchall())#
            for estado in estados :
                user=ModelUser.get_by_id(db,int(estado[1]))
                supervisor=ModelUser.get_by_id(db,int(user.id_supervisor))
                state=ModelState.get_by_id(db,estado[4])
                totest=ModelState.totalStates(db,user)
                if(compania==user.compania['nombre']):
                    Hist={'id':user.id,'id_solvo':user.id_solvo,'Firts Name':user.nombres,'Last Name':user.apellidos,'Supervisor':supervisor.nombres,'state':state.nombre,'time':estado[3].strftime('%Y-%m-%d %H:%M:%S'),'totest':totest[state.nombre]}
                    lHistor.append(Hist) 
            if not lHistor:
                
                return None
            return lHistor
        except Exception as ex:
            raise Exception(ex)