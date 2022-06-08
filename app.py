from flask import Flask, render_template, request, redirect, url_for,flash  
from flask_mysqldb import MySQL

app=Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='solvoweb'
mysql=MySQL(app)

# settings
app.secret_key='mysecretkey'

@app.route('/')
def index():
    return render_template('proto_solvo.html')
@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(port=3000,debug=True)