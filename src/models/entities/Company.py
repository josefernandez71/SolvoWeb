class Company():

    def __init__(self,id,nombre="") -> None:
        self.id=id
        self.nombre=nombre
        
    def __repr__(self):
       return "<id: " + str(self.id) +" compania: " + str(self.nombre) + ">"
   