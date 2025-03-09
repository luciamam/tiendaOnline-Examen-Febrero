from flask import Flask, render_template,request, redirect
from dotenv import load_dotenv
from formularios.forms import FormRegister

from flask_bootstrap import Bootstrap4


load_dotenv
import os

app=Flask(__name__)
Bootstrap4(app)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')







@app.route('/register')
def registrarse():
    form=FormRegister()
    return render_template('Register.html',form=form)



@app.route('/login')
def login():
    return "login "
 

if __name__=='__main__':
    app.run(debug=True)