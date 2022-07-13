# Controlador principal de la pagina web


#importaciones necesarias de flask
from email import message
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required,current_user

#controlador de configuracion 
from config import config
import json

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
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
# settings
app.secret_key='mysecretkey'

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

@app.route('/Show',methods=['GET', 'POST'])
def Show():
    return render_template('Show.html', users=ModelUser.Show(db))

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

#Lleva a la vista de editar usuario
@app.route('/editUsers/<int:id>', methods=['GET', 'POST'])
def editUsers(id):
    return render_template('EditUsers.html', users=ModelUser.edit(db, id))
    
#Edita el usuario seleccionado en la vista
@app.route('/Update', methods=['GET', 'POST'])
def Update():
    if request.method == 'POST':
        user = User(request.form['userid'],request.form['email'],0,request.form['solvoid'],request.form['name']
                ,request.form['lastname'],"activo",0)
        ModelUser.Update(db, user)
        flash('User edit successfuly')
        return redirect(url_for('Show'))
    else:
        return redirect(url_for('Show'))

@app.route('/changEstate/<int:id>', methods=['GET', 'POST'])
def changEstate(id):
    estado = ModelUser.traerEstado(db, id)
    if estado != None:
        ModelUser.State(db, id, estado)
        flash('State update successfuly')
        return redirect(url_for('Show'))
    else: 
        flash('Error state no update')
        return redirect(url_for('Show'))

@app.route('/addCity', methods=['GET', 'POST'])
def addCity():
    if request.method == 'POST':
        city = City(0, request.form['nombre_ciudad'])
        exists = ModelCompanyCity.ExistCity(db, city)
        if exists != None:
            flash("exists City")
            return render_template('addCity.html')
        else:
            ModelCompanyCity.addCity(db, city)
            return render_template('addCity.html')
    else:
        return render_template('addCity.html')

@app.route('/addCompany', methods=['GET', 'POST'])
def addCompany():
    if request.method == 'POST':
        city = Company(0, request.form['nombre_compania'])
        exists = ModelCompanyCity.ExistCompany(db, city)
        if exists != None:
            flash("exists City")
            return render_template('addCompany.html')
        else:
            ModelCompanyCity.addCompany(db, city)
            return render_template('addCompany.html')
    else:
        return render_template('addCompany.html')

@app.route('/ShowCompCity',methods=['GET', 'POST'])
def ShowCompCity():
    return render_template('companyCity.html', compCity=ModelCompanyCity.ShowCompCity(db))

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
    estado=ModelState.get_by_id(db,estadoactual.id_estado)
    hola=ModelState.totalStates(db,current_user)
    print(hola)
    return render_template('menu.html',estadoactual=estadoactual, estado=estado)

#Cambios de estado
@app.route('/changeState',methods=['POST'])
def changeState():
    response=None
    if request.method == 'POST':
        state=request.form['estado']        
        state1=ModelState.get_by_name(db,state)
        ModelState.call_procedure(db,current_user,current_user,state1.id)
        estadoactual=ModelState.estadoActual(db,current_user)
        state1=ModelState.get_by_id(db,estadoactual.id_estado)
        response={
            'estado':state1.__dict__,
            'estadoactual':estadoactual.__dict__}
        return json.dumps(response)

#Respuestas a error por no estar autorizado para acceder a la pagina   
def status_401(error):
    return redirect(url_for('login'))

#respuesta cuando no existe la ruta a la que intenta acceder
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

#inicio de la pagina 
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
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

