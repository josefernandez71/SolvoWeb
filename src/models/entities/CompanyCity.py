class CompanyCity():

    def __init__(self, id ,id_company ,id_city) -> None:
        self.id=id
        self.id_company=id_company
        self.id_city=id_city
        
    def __repr__(self):
       return "<id: "+ str(self.id) +" compania: "+ str(self.id_company) +" ciudad: "+ str(self.id_city)