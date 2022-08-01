# Controlador principal de la pagina web
#importaciones necesarias de flask

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from flask_socketio import SocketIO,emit,join_room,leave_room

#controlador de configuracion 
from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelState import ModelState
from models.ModelCompanyCity import ModelCompanyCity

# Entities:
from models.entities.User import User
from models.entities.State import State
from models.entities.City import City
from models.entities.Company import Company
from models.entities.CompanyCity import CompanyCity

#asignacion de variables generales 
app = Flask(__name__)
json = FlaskJSON(app)
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
# settings
app.secret_key='mysecretkey'
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
    ListSup=ModelUser.ListSup(db)
    ListCompCitys=ModelUser.CompanyCity(db)
    return render_template('user/AddUsers.html', ListSup=ListSup, ListCompCitys=ListCompCitys)

@app.route('/Show',methods=['GET', 'POST'])
def Show():
    return render_template('user/Show.html', users=ModelUser.Show(db))

    #creacion de usuario interprete y supervisor
@app.route('/addInterp',methods=['GET', 'POST'],)
def addInterp():
    if request.method == 'POST':   
        #validacion si intenta crear un interpreete o supervisor    
        if request.form['profile']=="supervisor":
            user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],request.form['compciu'],"ACTIVO",0)
            #Validacion si exite el supervisor
            logged_user = ModelUser.ExistsUser(db, user,"supervisor")                
        elif request.form['profile']=="interpreter":
            user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],request.form['compciu'],"ACTIVO",request.form['supervisor'])
            logged_user = ModelUser.ExistsUser(db, user,"interpreter")   
            #Validacion     
            #si existe el usuario, si no existe lo crea
        if logged_user != None:
            flash("exists User")
            return redirect(url_for('Show'))
        else:
            #valida si el desea crear supervisor o interprete
            if request.form['profile']=="supervisor":
                #crea el supervisor
                ModelUser.addSup(db, user) 
                #envia mensaje de confirmacion
                flash('Supervisor created successfully')             
                return redirect(url_for('Show'))
            elif request.form['profile']=="interpreter":
                #Crea interprete 
                ModelUser.addInterp(db, user)
                #confirma envia mensaje de confirmacion
                flash('Interpreter created successfully ')
                return redirect(url_for('Show'))             
            return redirect(url_for('Show'))
    else:
        return redirect(url_for('Show'))

#Lleva a la vista de editar usuario
@app.route('/editUsers/<int:id>', methods=['GET', 'POST'])
def editUsers(id):
    users = ModelUser.edit(db, id)
    ListCompCitys = ModelUser.CompanyCity(db)
    return render_template('user/EditUsers.html', ListCompCitys=ListCompCitys, users=users)
    
#Edita el usuario seleccionado en la vista
@app.route('/Update', methods=['GET', 'POST'])
def Update():
    if request.method == 'POST':
        if request.form['idsupervisor'] != 'None':
            user = User(request.form['userid'],request.form['email'],0,request.form['solvoid'],request.form['name']
                ,request.form['lastname'],request.form['compciu'],"activo",0)
            ModelUser.UpdateInt(db, user)
            flash('User Interpreter edit successfuly')
            return redirect(url_for('Show'))
        else:
            user = User(request.form['userid'],request.form['email'],0,request.form['solvoid'],request.form['name']
                ,request.form['lastname'],request.form['compciu'],"activo",request.form['idsupervisor'])
            ModelUser.UpdateSup(db, user)
            flash('User Supervisor edit successfuly')
            return redirect(url_for('Show'))
    else:
        return redirect(url_for('Show'))

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

#Lleva a la vista para registrar una ciudad
@app.route('/city', methods=['GET', 'POST'])
def city():
    return render_template('city/addCity.html')

# Registrar nueva ciudad
@app.route('/addCity', methods=['GET', 'POST'])
def addCity():
    if request.method == 'POST':
        city = City(0, request.form['nombre_ciudad'])
        exists = ModelCompanyCity.ExistCity(db, city)
        if exists != None:
            flash("exists City")
            return redirect(url_for('ShowCompCity'))
        else:
            flash("City create successfuly")
            ModelCompanyCity.addCity(db, city)
            return redirect(url_for('ShowCompCity'))
    else:
        return redirect(url_for('ShowCompCity'))

# Lleva a la vista de editar ciudad
@app.route('/editCity/<int:id>', methods=['GET', 'POST'])
def editCity(id):
    return render_template('city/editCity.html', citys=ModelCompanyCity.EditCity(db, id))

# Edita la ciudad seleccionada
@app.route('/updaCity', methods=['GET', 'POST'])
def updaCity():
    if request.method == 'POST':
        if request.form['idCity']:
            city = City(request.form['idCity'], request.form['nombre_ciudad'])
            ModelCompanyCity.updaCity(db, city)
            flash('City edit successfuly')
            return redirect(url_for('ShowCompCity'))
        else:
            flash('City no edit')
            return redirect(url_for('ShowCompCity'))
    else:
        return redirect(url_for('ShowCompCity'))

# Borrar ciudad seleccionada
@app.route('/deleteCity/<int:id>', methods=['GET', 'POST'])
def deleteCity(id):
    city = ModelCompanyCity.deleteCity(db, id)
    flash("City delete successfuly")
    return redirect(url_for('ShowCompCity', city=city))
    
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

#Lleva a la vista para registrar una compañia
@app.route('/company', methods=['GET', 'POST'])
def company():
    return render_template('company/addCompany.html')

# Registrar nueva compañia
@app.route('/addCompany', methods=['GET', 'POST'])
def addCompany():
    if request.method == 'POST':
        city = Company(0, request.form['nombre_compania'])
        exists = ModelCompanyCity.ExistCompany(db, city)
        if exists != None:
            flash("exists Company")
            return redirect(url_for('ShowCompCity'))
        else:
            ModelCompanyCity.addCompany(db, city)
            flash("Company create successfuly")
            return redirect(url_for('ShowCompCity'))
    else:
        return redirect(url_for('ShowCompCity'))

# Lleva a la vista de editar compañia
@app.route('/editCompany/<int:id>', methods=['GET', 'POST'])
def editCompany(id):
    return render_template('company/editCompany.html', companys=ModelCompanyCity.EditCompany(db, id))

# Edita la compañia seleccionada
@app.route('/updaCompany', methods=['GET', 'POST'])
def updaCompany():
    if request.method == 'POST':
        if editCompany(id) == request.form['idCompany']:
            company = Company(request.form['idCompany'], request.form['nombre_compania'])
            ModelCompanyCity.updaCompany(db, company)
            flash('Company edit successfuly')
            return redirect(url_for('ShowCompCity'))
        else:
            flash('Company no edit')
            return redirect(url_for('ShowCompCity'))
    else:
        return redirect(url_for('ShowCompCity'))

# Borrar compañia seleccionada
@app.route('/deleteCompany/<int:id>', methods=['GET', 'POST'])
def deleteCompany(id):
    company=ModelCompanyCity.deleteCompany(db, id)
    flash("Company delete successfuly")
    return redirect(url_for('ShowCompCity', company=company))

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

# Lista las Ciudades y Compañias creadas
@app.route('/ShowCompCity',methods=['GET', 'POST'])
def ShowCompCity():
    ListCitys = ModelCompanyCity.ListCity(db)
    ListCompanys = ModelCompanyCity.ListCompany(db)
    CompCitys = ModelCompanyCity.ShowCompCity(db)
    return render_template('companyCity/companyCity.html', ListCitys=ListCitys, ListCompanys=ListCompanys, CompCitys=CompCitys)

# Lista las Ciudades y Compañias creadas
@app.route('/addCompanyCity',methods=['GET', 'POST'])
def addCompanyCity():
    Citys = ModelCompanyCity.ListCity(db)
    Companys = ModelCompanyCity.ListCompany(db)
    return render_template('companyCity/addCompanyCity.html', Citys=Citys, Companys=Companys)

# Registrar nueva compañia con ciudad
@app.route('/saveCompanyCity', methods=['GET', 'POST'])
def saveCompanyCity():
    if request.method == 'POST':
        companyCity = CompanyCity(0, request.form['company'], request.form['city'])
        exists = ModelCompanyCity.ExistCompanyCity(db, companyCity)
        if exists != None:
            flash("Exists related city and company")
            return redirect(url_for('ShowCompCity'))
        else:
            ModelCompanyCity.addCompanyCity(db, companyCity)
            flash("Successfully related company and city")
            return redirect(url_for('ShowCompCity'))
    else:
        return redirect(url_for('ShowCompCity'))

# Lleva a la vista de editar compañia con ciudad
@app.route('/editCompanyCity/<int:id>', methods=['GET', 'POST'])
def editCompanyCity(id):
    Citys = ModelCompanyCity.ListCity(db)
    Companys = ModelCompanyCity.ListCompany(db)
    companyCitys = ModelCompanyCity.EditCompanyCity(db, id)
    return render_template('companyCity/editCompanyCity.html', Citys=Citys, Companys=Companys, companyCitys=companyCitys)

# Edita la compañia con ciudad seleccionada
@app.route('/updaCompanyCity', methods=['GET', 'POST'])
def updaCompanyCity():
    if request.method == 'POST':
        if editCompany(id) == request.form['id']:
            companyCity = CompanyCity(request.form['id'], request.form['company'], request.form['city'])
            ModelCompanyCity.updaCompany(db, companyCity)
            flash('Related company city edit successfuly')
            return redirect(url_for('ShowCompCity'))
        else:
            flash('Related company city no edit')
            return redirect(url_for('ShowCompCity'))
    else:
        return redirect(url_for('ShowCompCity'))

# Borrar compañia con ciudad seleccionada
@app.route('/deleteCompanyCity/<int:id>', methods=['GET', 'POST'])
def deleteCompanyCity(id):
    companyCity=ModelCompanyCity.deleteCompanyCity(db, id)
    flash("Related of Company and City delete")
    return redirect(url_for('ShowCompCity', companyCity=companyCity))

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

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
    if request.method == 'POST':
        return False
        
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
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)


    
    

#Consulta estado actual 
#SELECT ID_HISTORIAL,ID_INTERPRETER,ID_SOLVO,RESPONSABLE,HORA_INICIO,ID_ESTADO FROM HISTORIAL WHERE ID_INTERPRETER=2 AND TEMP_BOOLEAN=1
#reporte y sumas 
#SELECT * FROM historial where HORA_INICIO like '%2022-06-13%' and HORA_FINAL <> 'null' order by id_estado ;



# @app.route('/EditUsers/<int:id>',methods=['GET', 'POST'])
# def EditUsers(id):
#     if request.method == 'POST':
#         if request.form['profile']=="supervisor":
#             user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
#                     ,request.form['lastname'],"activo",0)
#             #Validacion si exite el supervisor
#             logged_user = ModelUser.ExistsUser(db, user,"supervisor")                
#         elif request.form['profile']=="interpreter":
#             user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
#                     ,request.form['lastname'],"activo",request.form['supervisor'])
#             logged_user = ModelUser.ExistsUser(db, user,"interpreter")    
#             #si existe el usuario, si no existe lo crea
#         if logged_user != None:
#             flash("exists User")
#             return render_template('EditUsers.html')
#         else:
#             #valida si el desea crear supervisor o interprete
#             if request.form['profile']=="supervisor":
#                 #crea el supervisor
#                 ModelUser.addSup(db, user) 
#                 #envia mensaje de confirmacion
#                 flash('Supervisor created successfully')             
#                 return render_template('Show.html')
#             elif request.form['profile']=="interpreter":
#                 #Crea interprete 
#                 ModelUser.addInterp(db, user)
#                 #confirma envia mensaje de confirmacion
#                 flash('Interpreter created successfully ')
#                 return render_template('Show.html')            
#             return render_template('EditUsers.html')
#     else:
#         return redirect(url_for('EditUsers.html'))

# @app.route('/inactivate/<int:id>', method='GET')
# def inactivate(id):
#     return render_template('Show.html', users=ModelUser.inactivate(db, User.id))

