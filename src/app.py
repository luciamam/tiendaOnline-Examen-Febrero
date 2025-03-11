from flask import Flask, render_template,request, redirect,url_for,flash
from dotenv import load_dotenv
from formularios.forms import FormRegister,FormLogin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash,check_password_hash

from flask_bootstrap import Bootstrap4


load_dotenv
import os

app=Flask(__name__)
Bootstrap4(app)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

# vamos a crear la conexion con la base de datos 
client=MongoClient("mongodb://localhost:27017/")
#creamos la base de datos 
db=client['examenfebrero']
#creamos la collection
users_collection=db['usuarios']



@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/register')
def mostrar_formulario_register():
    form=FormRegister()
    
    return render_template('Register.html',form=form)

@app.route('/register',methods=['POST'])
def registrarse():
    data=request.form
    usuario={
        "name":data["name"],
        "email":data["email"],
        "password":generate_password_hash(data["password"])
    }
    #ahora vamos a introducir este diccionario creado para insertarlo en la  nuestra collection
    users_collection.insert_one(usuario)
    return redirect(url_for('perfil'))



@app.route('/perfil')
def perfil():
    return "bienvenido "

@app.route('/login')
def mostrar_login():
    form=FormLogin()
    return render_template('Login.html',form=form)


@app.route('/login',methods=['POST'])
def iniciar_sesion():
    #consigo el email y el password de la peticion 
    email=request.form.get('email')
    password=request.form.get('password')

    #buscamos en nuesta collection el docuemento que tenga este correo , y extraemos este usuario , nos devuelve todo el objeto con todas sus propiedades 
    usuario =users_collection.find_one({"email":email})
    print(usuario)
    if usuario:
        if check_password_hash(usuario["password"],password) :
            return redirect(url_for('perfil')) 
        else :
            flash("contraseña incorrecta","danger")
            
            return redirect(url_for('iniciar_sesion'))

    else:
        flash("usuario no registrado","danger")
       
        return   redirect(url_for('iniciar_sesion'))
    


@app.errorhandler(404)
def pagina_404(error):
    return render_template('Pagina_404.html')




if __name__=='__main__':
    app.run(debug=True)