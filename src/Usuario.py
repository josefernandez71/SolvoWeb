
from flask import render_template, request, redirect, url_for, flash
#from flask_json import FlaskJSON
from flask_login import  login_user, logout_user, login_required,current_user
import flask
#from flask_cors import CORS
#controlador de configuracion 
# Models:
from models.ModelUser import ModelUser
from models.ModelState import ModelState
# Entities:
from models.entities.User import User

import socket
#ruta raiz de la pagina
usuarios=flask.Blueprint('Usuario',__name__,url_prefix="/usuario")
#db=mysqlconnect()
#db=MySQLdb(app)
#Direccionamiento a pagina de pagina de administracion de usuarios 
@usuarios.route('/AdminUser',methods=['GET', 'POST'])
@login_required
def AdminUser():
    from app import getdb
    db=getdb()
    return render_template('AddUsers.html',ListSup=ModelUser.ListSup(db))
    #creacion de usuario interprete y supervisor
@usuarios.route('/addInterp',methods=['GET', 'POST'],)
def addInterp():
    if request.method == 'POST':   
        #validacion si intenta crear un interpreete o supervisor    
        if request.form['profile']=="supervisor":
            user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],"activo",0)
            #Validacion si exite el supervisor
            logged_user = ModelUser.ExistsUser(user,"supervisor")                
        elif request.form['profile']=="interpreter":
            user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],"activo",request.form['supervisor'])
            logged_user = ModelUser.ExistsUser(user,"interpreter")   
            #Validacion     
            #si existe el usuario, si no existe lo crea
        if logged_user != None:
            flash("exists User")
            return redirect(url_for('AdminUser'))
        else:
            #valida si el desea crear supervisor o interprete
            if request.form['profile']=="supervisor":
                #crea el supervisor
                ModelUser.addSup(user) 
                #envia mensaje de confirmacion
                flash('Supervisor created successfully')             
                return redirect(url_for('AdminUser'))
            elif request.form['profile']=="interpreter":
                #Crea interprete 
                ModelUser.addInterp(user)
                #confirma envia mensaje de confirmacion
                flash('Interpreter created successfully ')
                return redirect(url_for('AdminUser'))             
            return redirect(url_for('AdminUser'))
    else:
        return redirect(url_for('AdminUser'))
    
#Validacion de Inicio de sesion
@usuarios.route('/login',methods=['GET', 'POST'])
def login():
    from app import getdb
    db=getdb()
    if request.method == 'POST':
        user = User(0, request.form['user'],None,None, request.form['pass'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.contrasena:
                #inicio sesion correctamente
                print (logged_user)
                login_user(logged_user)
                #print(current_user)
                ModelState.call_procedure(db,current_user,current_user,4)
                return redirect(url_for('menu.menu'))
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
 
