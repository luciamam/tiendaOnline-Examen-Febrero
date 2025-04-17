from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, PasswordField, ValidationError,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo




class FormRegister(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=4,max=20)])
    email=EmailField('Email',validators=[DataRequired(),Length(min=12,max=40)])
    password=PasswordField('password',validators=[DataRequired(),Length(min=4,max=12),EqualTo('confirm')])
    confirm=PasswordField('Repeat',validators=[DataRequired(),Length(min=4,max=12)])
    submit=SubmitField('Registrarse')



class FormLogin(FlaskForm):
    
    email=EmailField('Email',validators=[DataRequired(),Length(min=12,max=40)])
    password=PasswordField('password',validators=[DataRequired(),Length(min=4,max=12)])
    submit=SubmitField('iniciar sesion')


