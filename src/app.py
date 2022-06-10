from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required


from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# settings
app.secret_key='mysecretkey'

@app.route('/')
def index():
    return redirect(url_for('login'))
@app.route('/AdminUser',methods=['GET', 'POST'])
def AdminUser():
    return render_template('AddUsers.html')

@app.route('/addInterp',methods=['GET', 'POST'])
def addInterp():
    if request.method == 'POST':
        user = User(0,request.form['email'],request.form['pass'],request.form['solvoid'],request.form['name']
                    ,request.form['lastname'],"activo",1)
        if request.form['profile']=="supervisor":
            logged_user = ModelUser.ExistsUser(db, user,"supervisor")                
        elif request.form['profile']=="interpreter":
            logged_user = ModelUser.ExistsUser(db, user,"interpreter")        
        if logged_user != None:
            flash("exists User")
            return redirect(url_for('AdminUser'))
        else:
            if request.form['profile']=="supervisor":
                ModelUser.addSup(db, user)              
                print("supervisor151")
                return redirect(url_for('AdminUser'))
            elif request.form['profile']=="interpreter":
                ModelUser.addInterp(db, user)
                print("interpreter2132")   
                return redirect(url_for('AdminUser'))             
            
            return redirect(url_for('AdminUser'))
    else:
        return redirect(url_for('AdminUser'))
    

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['user'], request.form['pass'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.contrasena:
                login_user(logged_user)
                return redirect(url_for('menu'))
            else:
                flash("Invalid password...")
                return render_template('proto_Solvo.html')
        else:
            flash("User not found...")
            return render_template('proto_Solvo.html')
    else:
        return render_template('proto_Solvo.html')

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

     
    
def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()