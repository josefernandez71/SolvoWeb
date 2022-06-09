from flask import Flask, render_template, request, redirect, url_for,flash  
from flask_mysqldb import MySQL

app=Flask(__name__)

#Mysql connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='solvo'
mysql=MySQL(app)

# settings
app.secret_key='mysecretkey'

@app.route('/')
def index():
    return render_template('proto_solvo.html')
@app.route('/menu',methods=['POST'])
def menu():
    data=none
    if request.method=='POST':
        
        usuario=request.form['user']
        password=request.form['pass']
        if usuario !="" and password != "":
            cur=mysql.connection.cursor()        
            cur.execute('select * from usuarios where name=%s and passwd=%s',(usuario,password))
            data=cur.fetchall()           
            try:
                if data!=none:
                    return render_template('menu.html', contact=data[0])
            except Exception as e:
                print ("No existe el usuario",sys.exc_info()[0])
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return render_template('proto_solvo.html')

if __name__ == '__main__':
    app.run(port=3000,debug=True)