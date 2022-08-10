from http.client import NotConnected
from flask import Flask 
from estados import estados
from Usuario import usuarios
from flask_mysqldb import MySQL
 

def init_app():
    app=Flask(__name__)
    #configuracion de la app 
    app.secret_key='mysecretkey'
    #configuracion de la Base de datos 
    app.config['MYSQL_HOST']='localhost'
    app.config['MYSQL_USER']='root'
    app.config['MYSQL_PASSWORD']=''
    app.config['MYSQL_DB']='solvo'
    #se agregan los blueprints para segmentar las rutas de la pagina web 
    app.register_blueprint(estados)
    app.register_blueprint(usuarios)
    db=MySQL(app)
    return app,db
 