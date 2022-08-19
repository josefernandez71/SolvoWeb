# Controlador principal de la pagina web
#importaciones necesarias de flask

from ast import And, If
from operator import and_, length_hint, truediv
from pickle import FALSE, TRUE
import re
from traceback import print_tb
from flask import render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, logout_user, login_required,current_user
from flask_socketio import SocketIO,emit,join_room,leave_room
from flask_cors import CORS
from init import init_app
import json
#controlador de configuracion 

# Models:
from models.ModelUser import ModelUser
from models.ModelState import ModelState
from models.ModelCompanyCity import ModelCompanyCity

# Entities:
from models.entities.User import User
from models.entities.City import City
from models.entities.Company import Company
from models.entities.CompanyCity import CompanyCity

import time

#asignacion de variables generales 
app,db = init_app()
CORS(app)
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
# settings
app.secret_key='mysecretkey'
socket=SocketIO(app,async_mode="threading",async_handlers=True)
def getdb():
    return db


#Obtiene usuario en la base de datos por el Id 
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)
@app.route('/')
def index():
    print(getdb())
    return redirect(url_for('Usuario.login'))

@app.route('/RTS',methods=['GET', 'POST'])
def RTS():
    listRT=ModelState.listRTS(db,current_user.compania)
    return render_template('RealTime.html',compania=current_user.compania, listRTS=listRT)
#Respuestas a error por no estar autorizado para acceder a la pagina   
def status_401(error):
    return redirect(url_for('Usuario.login'))

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
    print(room)
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
    emit('leave', username+" abandono la habitacion", to=room['room'])
 
@socket.on('event')
def event(json):
    print ('estamos en evento',json)
    emit('event',json,broadcast=True)

@socket.on('connect')
def test_connect():
    print ("conectado")
    emit('my response','Connected')

@socket.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    return True

#Cerrar sesion    
@app.route('/logout')
def logout():
    print(current_user)
    c={'room': current_user.compania['nombre']}
    ModelState.call_procedure(db,current_user,current_user,1)
    #join(c)
    message=dict({'message':{'logout':True,'id':current_user.id}})
    socket.emit('chat',json.dumps(message['message']),to =c['room'])    #elimina la sesion iniciada 
    #leave(c)
    logout_user()
    return redirect(url_for('Usuario.login'))



#Direccionamiento a pagina de pagina de administracion de usuarios 
@app.route('/AdminUser',methods=['GET', 'POST'])
@login_required
def AdminUser():
    ListSup=ModelUser.ListSup(db)
    ListAdmin=ModelUser.ListAdmin(db)
    ListTeam=ModelUser.ListTeam(db)
    ListPerfil=ModelUser.perfil(db)
    citys = ModelUser.listCity(db)
    companys = ModelUser.listCompany(db)
    return render_template('user/AddUsers.html', ListSup=ListSup, ListAdmin=ListAdmin, ListTeam=ListTeam, ListPerfil=ListPerfil, citys=citys, companys=companys)

@app.route('/Show',methods=['GET', 'POST'])
def Show():
    return render_template('user/Show.html', users=ModelUser.Show(db))

    #creacion de usuario interprete y supervisor
@app.route('/addInterp',methods=['GET', 'POST'],)
def addInterp():
    if request.method == 'POST':   
        #validacion si intenta crear un interpreete o supervisor    
        if request.form['perfil']== "1":
            user = User(0,request.form['email'],request.form['comp'],request.form['ciu'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],request.form['perfil'],"ACTIVO",0)
            #Validacion si exite el Admin
            logged_user = ModelUser.ExistsUser(db, user)
            relacion = compciu(request.form['comp'],request.form['ciu'])
        elif request.form['perfil']== "2":
            user = User(0,request.form['email'],request.form['comp'],request.form['ciu'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],request.form['perfil'],"ACTIVO",request.form['administrator'])
            #Validacion si exite el Supervisor
            logged_user = ModelUser.ExistsUser(db, user)
            relacion = compciu(request.form['comp'],request.form['ciu'])
        elif request.form['perfil']== "3":
            user = User(0,request.form['email'],request.form['comp'],request.form['ciu'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],request.form['perfil'],"ACTIVO",request.form['supervisor'])
            #Validacion si exite el TeamLeader
            logged_user = ModelUser.ExistsUser(db, user)
            relacion = compciu(request.form['comp'],request.form['ciu'])
        elif request.form['perfil']== "4":
            user = User(0,request.form['email'],request.form['comp'],request.form['ciu'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],request.form['perfil'],"ACTIVO",request.form['teamleader'])
            #Validacion si exite el Interpreter
            logged_user = ModelUser.ExistsUser(db, user)
            relacion = compciu(request.form['comp'],request.form['ciu'])

        #si existe el usuario, si no existe lo crea
        if logged_user != None:
            flash("exists User")
            return redirect(url_for('Show'))
        else:
            #valida si el desea crear administrador, supervisor, team leader o interprete
            if request.form['perfil']=="1" and relacion==True:
                #crea el administrador
                ModelUser.addAdmin(db, user) 
                #envia mensaje de confirmacion
                flash('Administrator created successfully')             
                return redirect(url_for('Show'))
            elif request.form['perfil']=="2" and relacion==True:
                #crea el supervisor
                ModelUser.addSup(db, user) 
                #envia mensaje de confirmacion
                flash('Supervisor created successfully')             
                return redirect(url_for('Show'))
            elif request.form['perfil']=="3" and relacion==True:
                #crea el team leader
                ModelUser.addSup(db, user) 
                #envia mensaje de confirmacion
                flash('Team leader created successfully')             
                return redirect(url_for('Show'))
            elif request.form['perfil']=="4" and relacion==True:
                #crea el interprete 
                ModelUser.addSup(db, user)
                #confirma envia mensaje de confirmacion
                flash('Interpreter created successfully ')
                return redirect(url_for('Show'))
            else: 
                flash('Error with profile or selected city with company')
                return redirect(url_for('Show'))
    else:
        return redirect(url_for('Show'))

#Lleva a la vista de editar usuario
@app.route('/editUsers/<int:id>', methods=['GET', 'POST'])
def editUsers(id):
    users = ModelUser.edit(db, id)
    ListSup = ModelUser.ListSup(db)
    ListAdmin = ModelUser.ListAdmin(db)
    ListTeam = ModelUser.ListTeam(db)
    ListPerfil = ModelUser.perfil(db)
    citys = ModelUser.listCity(db)
    companys = ModelUser.listCompany(db)
    return render_template('user/EditUsers.html', citys=citys, companys=companys, ListAdmin=ListAdmin, ListTeam=ListTeam, ListSup=ListSup, ListPerfil=ListPerfil, users=users)
    
#Edita el usuario seleccionado en la vista
@app.route('/Update', methods=['GET', 'POST'])
def Update():
    if request.method == 'POST':
        if request.form['perfil'] == "1":
            user = User(request.form['userid'],request.form['email'],request.form['comp'],request.form['ciu'],0,request.form['solvoid'],request.form['name']
                ,request.form['lastname'],request.form['perfil'],"ACTIVO",0)
            relacion = compciu(request.form['comp'], request.form['ciu'])
            if relacion == True:
                ModelUser.UpdateSup(db, user)
                flash('User Interpreter edit successfuly')
                return redirect(url_for('Show'))
            else:
                flash('The selected Company is not located in the city')
                return redirect(url_for('Show'))

        if request.form['perfil'] == "2":
            user = User(request.form['userid'],request.form['email'],request.form['comp'],request.form['ciu'],0,request.form['solvoid'],request.form['name']
                ,request.form['lastname'],request.form['perfil'],"ACTIVO",request.form['administrator'])
            relacion = compciu(request.form['comp'], request.form['ciu'])
            if relacion == True:
                ModelUser.UpdateSup(db, user)
                flash('User Supervisor edit successfuly')
                return redirect(url_for('Show'))
            else:
                flash('The selected Company is not located in the city')
                return redirect(url_for('Show'))

        if request.form['perfil'] == "3":
            user = User(request.form['userid'],request.form['email'],request.form['comp'],request.form['ciu'],0,request.form['solvoid'],request.form['name']
                ,request.form['lastname'],request.form['perfil'],"ACTIVO",request.form['supervisor'])
            relacion = compciu(request.form['comp'], request.form['ciu'])
            if relacion == True:
                ModelUser.UpdateSup(db, user)
                flash('User Team leader edit successfuly')
                return redirect(url_for('Show'))
            else:
                flash('The selected Company is not located in the city')
                return redirect(url_for('Show'))

        elif request.form['perfil'] == "4":
            user = User(request.form['userid'],request.form['email'],request.form['comp'],request.form['ciu'],0,request.form['solvoid'],request.form['name']
                ,request.form['lastname'],request.form['perfil'],"ACTIVO",request.form['teamleader'])
            relacion = compciu(request.form['comp'], request.form['ciu'])
            if relacion == True:
                ModelUser.UpdateSup(db, user)
                flash('User Interpreter edit successfuly')
                return redirect(url_for('Show'))
            else:
                flash('The selected Company is not located in the city')
                return redirect(url_for('Show'))
    else:
        return redirect(url_for('Show'))

def compciu(comp, ciu):
    lista = ModelUser.getCompCiuTodos(db)
    for listacc in lista:
        if listacc['id'] >=0 and listacc['ciudad']['id']==int(ciu) and listacc['compania']['id']==int(comp):
            return True
    return False

@app.route('/ShowUser/<int:id>', methods=['GET', 'POST'])
def ShowUser(id):
    perfiles = ModelUser.perfil(db)
    listUser = ModelUser.user(db)
    listCompCity = ModelUser.CompanyCity(db)
    showUser = ModelUser.ShowUser(db, id)
    return render_template('user/showUser.html', perfiles=perfiles, listUser=listUser, listCompCity=listCompCity, showUser=showUser)

@app.route('/inactive/<int:id>', methods=['GET', 'POST'])
def inactive(id):
    estado = ModelUser.traerEstado(db, id)
    if estado != None:
        ModelUser.State(db, id, estado)
        flash('State update successfuly')
        return redirect(url_for('Show'))
    else: 
        flash('Error state no update')
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
#inicio de la pagina 
if __name__ == '__main__':
    app.run(app)
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    login_manager_app.init_app(app)

#Consulta estado actual 
#SELECT ID_HISTORIAL,ID_INTERPRETER,ID_SOLVO,RESPONSABLE,HORA_INICIO,ID_ESTADO FROM HISTORIAL WHERE ID_INTERPRETER=2 AND TEMP_BOOLEAN=1
#reporte y sumas 
#SELECT * FROM historial where HORA_INICIO like '%2022-06-13%' and HORA_FINAL <> 'null' order by id_estado ;
