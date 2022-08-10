import flask 
from flask import render_template, request
from models.ModelUser import ModelUser
from models.ModelState import ModelState
from flask_login import login_required,current_user
from flask_mysqldb import MySQLdb
estados=flask.Blueprint('menu',__name__,url_prefix='/estados')
#db=mysqlconnect()
#db=MySQLdb(app)
#direccionamiento a Pagina de estados 
@estados.route('/menu')
@login_required
def menu():
    from app import getdb
    db=getdb()
    estadoactual=ModelState.estadoActual(db,current_user)
    print(estadoactual)
    state1=ModelState.get_by_id(db,estadoactual.id_estado)
    totalStates=ModelState.totalStates(db,current_user)
    sup=ModelUser.get_by_id(db,estadoactual.user['id_supervisor']).nombres
    response={
        'estado':state1.__dict__,
        'estadoactual':estadoactual.__dict__,
        'totalStates':totalStates,
        'logout':False,
        'id': 0,
        'sup':sup
    }
    return render_template('menu.html',data=dict(response))
#Cambios de estado
@estados.route('/changeState',methods=['POST'])
def changeState():
    from app import getdb
    db=getdb()
    response=None
    if request.method == 'POST':
        state=request.form['estado']      
        state1=ModelState.get_by_name(db,state)
        ModelState.call_procedure(db,current_user,current_user,state1.id)
        estadoactual=ModelState.estadoActual(db,current_user)
        if(estadoactual!=None):
            state1=ModelState.get_by_id(db,estadoactual.id_estado)
        totalStates=ModelState.totalStates(db,current_user)  
        print(totalStates)
        response={
            'estado':state1.__dict__,
            'estadoactual':estadoactual.__dict__,
            'totalStates':totalStates,
            'logout': False,
            'id':0,
            }  
        response=dict(response)
        return response
    return None