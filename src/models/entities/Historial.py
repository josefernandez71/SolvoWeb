class Historial():

    def __init__(self,id,user,responsable,HORA_INICIO,HORA_FINAL=None,id_estado=0,totaltime=None) -> None:
        self.id=id
        self.user=user
        self.responsable=responsable
        self.hora_inicio=HORA_INICIO
        self.hora_final=HORA_FINAL
        self.id_estado=id_estado
        self.totaltime=totaltime
        
    def __repr__(self):
       return "<id: " + str(self.id) +" usuario: " + str(self.user)  +" fecha inicio: " + str(self.hora_inicio) +"fecha fin: " + str(self.hora_final)+ " estado : " + str(self.id_estado)+"total : " + str(self.totaltime)
   