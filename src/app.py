from flask import Flask, render_template,request, redirect,url_for
from dotenv import load_dotenv
from formularios.forms import FormRegister,FormLogin
from pymongo import MongoClient

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

@app.route('/register',methods=['GET','POST'])
def registrarse():
    form=FormRegister()
    

    if request.method=='POST':
        data=request.form

        usuario={
            "name":data["name"],
            "email":data["email"],
            "password":data["password"],
        }
        #GUARDAMOS LOS DATOS EN LA BASE DE DATOS EN nuestra collection 
        users_collection.insert_one(usuario)
        return redirect(url_for('perfil'))


    
    return render_template('Register.html',form=form)


@app.route('/perfil')
def perfil():
    return "bienvenido "

@app.route('/login')
def login():
    form=FormLogin()
    return render_template('Login.html',form=form)






if __name__=='__main__':
    app.run(debug=True)