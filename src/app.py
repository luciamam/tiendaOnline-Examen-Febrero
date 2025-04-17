from flask import Flask, render_template,request, redirect,url_for,flash,make_response
from dotenv import load_dotenv
from formularios.forms import FormRegister,FormLogin
from pymongo import MongoClient
from werkzeug.security import generate_password_hash,check_password_hash
#para jwt
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity,create_access_token,unset_access_cookies
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
#client=MongoClient("mongodb://localhost:65432/")
#conexion con atltas 
client=MongoClient("mongodb+srv://lucia-dos:123456lucia@despliegueflask.vlrjgyf.mongodb.net/?retryWrites=true&w=majority&appName=despliegueFlask")
#client=MongoClient("mongodb://localhost:27017/")
#creamos la base de datos 
db=client['examenfebrero']
#creamos la collection
users_collection=db['usuarios']


#para usar el contador 
contador=0



@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/register')
def mostrar_formulario_register():
    form=FormRegister()
    cookies=request.cookies
    cookie=cookies.get('access_token_cookie')
    print("cookie en el register",cookie)
    #print("dict cookie",cookies)
    if cookie :
        return redirect(url_for('perfil'))
    
    
    return render_template('Register.html',form=form)

@app.route('/register',methods=['POST'])
def registrarse():
    global contador
    
    data=request.form
    usuario={
        "name":data["name"],
        "email":data["email"],
        "password":generate_password_hash(data["password"]),
        "contador":1,
        ########### dia 05/04
        "carrito":[]
        
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

    cookies=request.cookies
    cookie=cookies.get('access_token_cookie')
    #print("dict cookie",cookies)
    if cookie :
        return redirect(url_for('perfil'))

    return render_template('Login.html',form=form)

@app.route('/login',methods=['POST'])
def iniciar_sesion():
    #consigo el email y el password de la peticion 
    email=request.form.get('email')
    password=request.form.get('password')
    usuario =users_collection.find_one({"email":email})# busca el usuario con este email pero devuelve todo el objeto del usuario 
    #print("el usuario es el siguiente",usuario)
    
    if usuario:
        if check_password_hash(usuario["password"],password) :
            
            # id_usuario=usuario.inserted_id por que no estamos insertando usuario 
            #print("este es el id de mi usuario ",usuario['_id'])
           
            #con esto voy a crear el token 
            response=make_response(redirect(url_for('perfil')))
            id_usuario=str(usuario['_id'])  #lo paso a str para no guarda el id en el tipo de dato ObjectId 
            usuario=users_collection.find_one({"_id":ObjectId(id_usuario)})
            print("es el usuario en el LOGIN",usuario)
            contador=usuario["contador"]
            contador+=1
            #actualizar un valor en la base de datos 
            users_collection.update_one({"email":email},{'$set':{'contador':contador}})
            
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
    id_usuario=json.loads(id_usuario)  #y aqui es donde hago a diccionario u objeto 
    current_user=users_collection.find_one({"_id":ObjectId(id_usuario['id'])})
    print("este el current_user",current_user)
    name=current_user['name']
    contador=current_user['contador']



    return render_template("Profile.html",name=name,contador=contador )


@app.route('/logout')
def cerrar_sesion():
    response=make_response(redirect(url_for('mostrar_login')))
    unset_access_cookies(response) #quita todas las cookies de acceso 
    return response


@app.route('/tienda2')
def  mostrar_tienda2():
    productos=list(db.productos.find({},{"_id":1,"precio":1,"nombre":1}))
    for producto in productos:
        id=str(producto['_id'])
        producto["ruta"]='/producto/'+id
    return render_template('Productos.html',productos=productos)



#dia 05

@app.route('/tienda')
@jwt_required(locations=['cookies'])
def mostrar_tienda():
    #hemos realizado un script entonces necesitamos la variable que hemos o la base de daos 
    #el dato  me sale vacio 
    cookie=get_jwt_identity()
    cookie=cookie.replace("'",'"')
    cookie_id=json.loads(cookie)['id']
    #para acceder a collection de productos y traerme todos los producto pero con esta escpecifacion de los campos en la baase de datos  lo 
    #lo guardo en una variable porque  para pasar un valor  a jinja tiene que variable y valor 
    productos=list(db.productos.find({},{"_id":1,"nombre":1,"descripcion":1}))


    # #dia 07/04/2025 no es necesario 
    # usuario=db.usuarios.find_one({"_id":ObjectId(cookie_id)})
    # id_usuario=usuario['_id']
    
    

    return render_template('Tienda.html',productos=productos)

#dia 04
@app.route('/producto/<id>')
def mostrar_producto(id):
    producto=db.productos.find_one({"_id":ObjectId(id)})
    print("soy el producto",producto)

    return render_template("Producto.html",producto=producto)


#hoy  dia 05  
@app.route('/anydircarrito/<id>')
@jwt_required(locations=['cookies'])
def addCarrito(id):
    cookie=get_jwt_identity()
    cookie=cookie.replace("'",'"')
    id_usuario_actual=json.loads(cookie)['id']
    print("id_usuario en carrito",id_usuario_actual)
    #usuario=list(db.usuarios.find({"_id":ObjectId(id_usuario_actual)}))
    producto=db.productos.find_one({"_id":ObjectId(id)})
    #lista_carrito=[]
    #lista_carrito.append(producto)  
    #actualizar el usuario , porque le voy modificar los datos lo que hacemos es actualizar el usuario

    #voy a recuperrar ella clave carrito
    usuario=db.usuarios.find_one({"_id":ObjectId(id_usuario_actual)})
    #recupero  la clave carrito y luego le añado el producto
    lista_carrito=usuario['carrito']
    lista_carrito.append(producto)
    print("lista carritodb",lista_carrito,type(lista_carrito))
    db.usuarios.update_one({"_id":ObjectId(id_usuario_actual)},{"$set":{"carrito":lista_carrito}})
    
    print("usuario actulizado")
    #dia 08/03
    return  redirect(url_for('mostrar_tienda'))


#dia 07-08
@app.route('/carrito')
@jwt_required(locations=['cookies'])
def carrito():
    cookie=get_jwt_identity()
    cookie=cookie.replace("'",'"')
    id_usuario=json.loads(cookie)['id']
    usuario=db.usuarios.find_one({"_id":ObjectId(id_usuario)})
    #ahora voy a recuperar el campo carrito del usuuario
    print("usuario dentro de carrito",usuario)
    carrito=usuario['carrito']
    print("carrito",type(carrito),carrito)
    if len(carrito):
        return  render_template('Carrito.html',carrito=carrito)
   
    #return flash("no tienes productos","")
    return "tu carrito esta vacia"


######DIA 08/04
#####################################  RUTA ADMIN ####################################

@app.route('/admin')
def panel_admin():
    usuarios=list(db.usuarios.find({}))
    return render_template('Panel_admin.html',usuarios=usuarios)



@app.route('/admin/usuario/anydir',methods=['GET','POST'])
def anydir_usuario():
    if request.method=='POST':
        formulario=request.form
        db.usuarios.insert_one({
             "name":formulario['name'],
             "email":formulario['email'],
             "password":formulario['password'],
             "contador":0,
             "carrito":[]

        })
        return redirect(url_for('panel_admin'))

    return render_template('Anydir_Usuario.html')





#yo misma para editar al usuarios   dia 08/04
@app.route('/admin/usuario/editar/<id>',methods=['GET','POST'])
def editar(id):

    datos=request.form# estos son los nuevos del formularip 
    if request.method=='POST':
        #BUSCO AL USARIO 

        usuario=db.usuarios.find_one({"_id":ObjectId(id)})
        db.usuarios.update_one({"_id":ObjectId(id)},{"$set":{"email":datos['email']}})
        return redirect(url_for('panel_admin'))
    return render_template('Editar_Usuario.html')




@app.route('/admin/usuario/datosUsuario/<id>')
def datosUsuario(id):
        usuario=db.usuarios.find_one({"_id":ObjectId(id)})
        return render_template("DatosUsuario.html",usuario=usuario)

#####################################################################
####dia 12/04

@app.route('/admin/productos')
def panel_admin_productos():
    productos=list(db.productos.find())

    return render_template('Panel_Admin_Productos.html',productos=productos)



@app.route('/admin/producto/editar/<id>')
def editar_producto(id):
    producto=db.productos.find({"_id":ObjectId(id)})
    data=request.form
    if request.method=='POST':
        db.productos.update_one({"_id":ObjectId(id)},{'$set':{
            "nombre":data['nombre'],
            "descripcio":data['descripcion'],
            "precio":data['precio']
        }})
        return redirect(url_for('panel_admin_productos'))
    return render_template('Editar_producto')
    





@app.errorhandler(404)
def pagina_404(error):
    return render_template('Pagina_404.html')


@jwt.unauthorized_loader
def manejo_token(mensaje):
    return redirect(url_for('registrarse'))


if __name__=='__main__':
    app.run(debug=True)