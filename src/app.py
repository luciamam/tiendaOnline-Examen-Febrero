from flask import Flask, render_template,request, redirect,url_for,flash,make_response
from dotenv import load_dotenv
from formularios.forms import FormRegister,FormLogin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash,check_password_hash
#para jwt
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity,create_access_token
#para el json
import json
#para poder leer el _id de  mongo 
from bson import ObjectId


from flask_bootstrap import Bootstrap4


load_dotenv
import os

app=Flask(__name__)
Bootstrap4(app)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
#para jwt
jwt=JWTManager(app)

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

    documento_usuario=users_collection.insert_one(usuario) #crear  un docuemento 
    id_usuario=documento_usuario.inserted_id # id es un tipo de dato ObjectId propio de MongoDB
    id_usuario=str(id_usuario)  #para quitarle el objetID
    #print("este es el id de mi usuario ",id_usuario)
    response=make_response(redirect(url_for('perfil')))
    #aqui en la cookie tenemos que enviarle el id sin ObjectId 
    create_token=create_access_token(identity=str({"id":id_usuario})) #CONVERTIMO EL OBJETO EN STR porse se guarda en la cookie, y esta guarda datos com str 
    response.set_cookie('access_token_cookie',create_token)
    
    return  response





@app.route('/login')
def mostrar_login():
    form=FormLogin()
    return render_template('Login.html',form=form)


@app.route('/login',methods=['POST'])
def iniciar_sesion():
    #consigo el email y el password de la peticion 
    email=request.form.get('email')
    password=request.form.get('password')

    
    usuario =users_collection.find_one({"email":email})# busca el usuario con este email pero devuelve todo el objeto del usuario 
    print("el usuario es el siguiente",usuario)
    if usuario:
        if check_password_hash(usuario["password"],password) :
             
            # id_usuario=usuario.inserted_id por que no estamos insertando usuario 
            #print("este es el id de mi usuario ",usuario['_id'])
            #con esto voy a crear el token 
            response=make_response(redirect(url_for('perfil')))
            id_usuario=str(usuario['_id'])  #lo paso a str para no guarda el id en el tipo de dato ObjectId 
            
            create_token=create_access_token(identity=str({"id":id_usuario}))
            response.set_cookie('access_token_cookie',create_token)
            return response
    

        else :
            flash("contraseña incorrecta","danger")
            
            return redirect(url_for('iniciar_sesion'))

    else:
        flash("usuario no registrado","danger")

        return   redirect(url_for('iniciar_sesion'))
    

@app.route('/perfil')
#donde queremos localizar el token 
@jwt_required(locations=["cookies"])
def perfil():
    id_usuario=get_jwt_identity() #{'id:"12222233232323232"} sigue siendo un str 
    print("el id_usuario en la ruta perfil ",id_usuario)
    #print("tipo de dato id_usuario",type(id_usuario))
    id_usuario=id_usuario.replace("'",'"') # utilizo replace para que tenga formato json 
    id_usuario=json.loads(id_usuario)  #y aqui es donde haga a diccionario u objeto 
    current_user=users_collection.find_one({"_id":ObjectId(id_usuario['id'])})
    print("este el current_user",current_user)
    name=current_user['name']

    return render_template("Profile.html",username=name)


@app.route('/tienda')
def  mostrar_tienda():
    return "hola tienda "



@app.errorhandler(404)
def pagina_404(error):
    return render_template('Pagina_404.html')


@jwt.unauthorized_loader
def manejo_token(mensaje):
    return redirect(url_for('registrarse'))


if __name__=='__main__':
    app.run(debug=True)