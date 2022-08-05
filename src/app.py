# Controlador principal de la pagina web
#importaciones necesarias de flask

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from flask_socketio import SocketIO,emit,join_room,leave_room
from flask_cors import CORS

#controlador de configuracion 
from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelState import ModelState

# Entities:
from models.entities.User import User
from models.entities.State import State

#asignacion de variables generales 
app = Flask(__name__)
app.secret_key='mysecretkey'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='solvo'
CORS(app)
json = FlaskJSON(app)
csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)
# settings
socket=SocketIO(app,async_mode="threading",async_handlers=True)

#Obtiene usuario en la base de datos por el Id 
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


#ruta raiz de la pagina
@app.route('/')
def index():
  return redirect(url_for('login'))

#Direccionamiento a pagina de pagina de administracion de usuarios 
@app.route('/AdminUser',methods=['GET', 'POST'])
@login_required
def AdminUser():
    return render_template('AddUsers.html',ListSup=ModelUser.ListSup(db))
    #creacion de usuario interprete y supervisor
@app.route('/addInterp',methods=['GET', 'POST'],)
def addInterp():
    if request.method == 'POST':   
        #validacion si intenta crear un interpreete o supervisor    
        if request.form['profile']=="supervisor":
            user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],"activo",0)
            #Validacion si exite el supervisor
            logged_user = ModelUser.ExistsUser(db, user,"supervisor")                
        elif request.form['profile']=="interpreter":
            user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],"activo",request.form['supervisor'])
            logged_user = ModelUser.ExistsUser(db, user,"interpreter")   
            #Validacion     
            #si existe el usuario, si no existe lo crea
        if logged_user != None:
            flash("exists User")
            return redirect(url_for('AdminUser'))
        else:
            #valida si el desea crear supervisor o interprete
            if request.form['profile']=="supervisor":
                #crea el supervisor
                ModelUser.addSup(db, user) 
                #envia mensaje de confirmacion
                flash('Supervisor created successfully')             
                return redirect(url_for('AdminUser'))
            elif request.form['profile']=="interpreter":
                #Crea interprete 
                ModelUser.addInterp(db, user)
                #confirma envia mensaje de confirmacion
                flash('Interpreter created successfully ')
                return redirect(url_for('AdminUser'))             
            return redirect(url_for('AdminUser'))
    else:
        return redirect(url_for('AdminUser'))
    
#Validacion de Inicio de sesion
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['user'], request.form['pass'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.contrasena:
                #inicio sesion correctamente
                login_user(logged_user)
                #print(current_user)
                return redirect(url_for('menu'))
            else:
                #contraseña incorrecta
                flash("Invalid password...")
                return render_template('proto_Solvo.html')
        else:
            #usuario no existe
            flash("User not found...")
            return render_template('proto_Solvo.html')
    else:
        return render_template('proto_Solvo.html')
 
#Cerrar sesion    
@app.route('/logout')
def logout():
    #elimina la sesion iniciada 
    logout_user()
    return redirect(url_for('login'))

#direccionamiento a Pagina de estados 
@app.route('/menu')
@login_required
def menu():
    estadoactual=ModelState.estadoActual(db,current_user)
    state1=ModelState.get_by_id(db,estadoactual.id_estado)
    totalStates=ModelState.totalStates(db,current_user)  
    response={
        'estado':state1.__dict__,
        'estadoactual':estadoactual.__dict__,
        'totalStates':totalStates
        }  
    
    return render_template('menu.html',data=dict(response))
#Cambios de estado
@app.route('/changeState',methods=['POST'])
def changeState():
    response=None
    if request.method == 'POST':
        state=request.form['estado']      
        state1=ModelState.get_by_name(db,state)
        #print(state1)
        ModelState.call_procedure(db,current_user,current_user,state1.id)
        
        estadoactual=ModelState.estadoActual(db,current_user)
        #print(estadoactual)
        if(estadoactual!=None):
            state1=ModelState.get_by_id(db,estadoactual.id_estado)
        totalStates=ModelState.totalStates(db,current_user)  
        print(totalStates)
        response={
            'estado':state1.__dict__,
            'estadoactual':estadoactual.__dict__,
            'totalStates':totalStates
            }  
        response=dict(response)
        return response
    return None
@app.route('/RTS',methods=['GET', 'POST'])
def RTS():
    
    return render_template('RealTime.html')
#Respuestas a error por no estar autorizado para acceder a la pagina   
def status_401(error):
    return redirect(url_for('login'))

#respuesta cuando no existe la ruta a la que intenta acceder
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


@socket.on('chat')
def chat(message):    
    print("chat "+str(message))
    emit('chat', message['message'], broadcast=True, to=message['room'])
    return True
   
@socket.on('join')
def join(room):
    username="mauro"  
    print("Join")
    print (room['room'])
    join_room(room['room'])
    emit('join', username+" se unio a la habitacion", to=room['room'])
    
@socket.on('leave')
def leave(room):
    username="mauro"   
    print("leave")
    leave_room(room['room'])
    #emit('leave', username+" abandono la habitacion", to=room['room'])

@socket.on('event')
def event(json):
    print ('estamos en evento',json)
    #emit('event',json,broadcast=True)

@socket.on('connect')
def test_connect(auth):
    print ("conectado")
   # emit('my response', {'data': 'Connected'})

@socket.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    return True


#inicio de la pagina 
#if __name__ == '__main__':
#    app.config.from_object(config['development'])
#    #csrf.init_app(app)
#    app.register_error_handler(401, status_401)
#    app.register_error_handler(404, status_404)
#    app.run(debug=True)


    
    

#Consulta estado actual 
#SELECT ID_HISTORIAL,ID_INTERPRETER,ID_SOLVO,RESPONSABLE,HORA_INICIO,ID_ESTADO FROM HISTORIAL WHERE ID_INTERPRETER=2 AND TEMP_BOOLEAN=1
#reporte y sumas 
#SELECT * FROM historial where HORA_INICIO like '%2022-06-13%' and HORA_FINAL <> 'null' order by id_estado ;