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
    app.config['MYSQL_HOST']='us-cdbr-east-06.cleardb.net'
    app.config['MYSQL_USER']='b1a740d25c64d3'
    app.config['MYSQL_PASSWORD']='bfe2d3e7'
    app.config['MYSQL_DB']='heroku_6d336b1af578ed7'
    #se agregan los blueprints para segmentar las rutas de la pagina web 
    app.register_blueprint(estados)
    app.register_blueprint(usuarios)
    db=MySQL(app)
    return app,db
 