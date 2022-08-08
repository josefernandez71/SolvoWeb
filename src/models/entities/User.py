from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self,id,correo_solvo,contrasena="",id_solvo=0,nombres="",apellidos="",id_compciu=0,perfil="",estado=0,id_supervisor=0) -> None:
        self.id=id
        self.id_solvo=id_solvo
        self.nombres=nombres
        self.apellidos=apellidos
        self.id_compciu=id_compciu
        self.perfil=perfil
        self.correo_solvo=correo_solvo
        self.estado=estado
        self.id_supervisor=id_supervisor
        self.contrasena=contrasena
        
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    def __repr__(self):
       return "<id: " + str(self.id) +"<contraseña: " + str(self.contrasena) + "; id_solvo: " + str(self.id_solvo) + "; nombres: " + str(self.nombres)  + "; apellidos: " + str(self.apellidos) + "; id_compciu:" + str(self.id_compciu) + "; perfil:"+ str(self.perfil) + "; correo: " + str(self.correo_solvo) + "; estado: " + str(self.estado) + "; id_supervisor:" + str(self.id_supervisor) +">"
     
print(generate_password_hash('Mauricio'))