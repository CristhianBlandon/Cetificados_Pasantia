from datetime import date
from wtforms import (Form, PasswordField, SelectField,
                     StringField, IntegerField, FileField, validators)
from wtforms.fields import EmailField
from wtforms.validators import DataRequired
from app.Database import coneccion_db

#---------------------------------------------------#
#          Datos Del Formulario De Email            #
#---------------------------------------------------#
class email(Form):
    
    def get_tipo_certificado_options():
        db = coneccion_db()    
        cursor = db.cursor()
        sql = '''SELECT * FROM  tipo_certificado'''
        cursor.execute(sql)
        options = [(str(result[0]), str(result[1])) for result in cursor.fetchall()]
        return options

    tipo_certificado = SelectField('Tipo Certificado', [DataRequired()], choices=get_tipo_certificado_options())
    
    
    tipo_doc = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Cédula de Extranjería', 'Cédula de Extranjería'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Pasaporte', 'Pasaporte'),
        ('NIT', 'NIT'),
        ('Otros', 'Otros')],)
    
    num_iden = IntegerField('Numero Identificación', [
                            validators.InputRequired(message='Este campo es obligatorio')])

    current_year = date.today().year
    years = [(str(y), str(y)) for y in range(2020, current_year + 1)]
    years = years[::-1]
    year = SelectField('Año de expedición de documento', [DataRequired()], choices=years)
   
#---------------------------------------------------#
#          Datos Del Formulario De Login            #
#---------------------------------------------------# 
class login(Form):
    
    email = EmailField('Correo Electronico', [
                       validators.InputRequired(message='Este campo es obligatorio')])

    password = PasswordField('Password', [validators.InputRequired(
        message='Este campo es obligatorio')])
    
#---------------------------------------------------#
#        Datos Del Formulario De Proveedores        #
#---------------------------------------------------#
class proveedores(Form):
    tipo_doc = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Cédula de Extranjería', 'Cédula de Extranjería'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Pasaporte', 'Pasaporte'),
        ('NIT', 'NIT'),
        ('Otros', 'Otros')],)
    
    num_iden = IntegerField('Numero Identificación', [
                            validators.InputRequired(message='Este campo es obligatorio')])

    nombre_razonsocial = StringField('Nombre o Razon Social', [validators.InputRequired(
        message='Este campo es obligatorio')])
    
    email = EmailField('Correo Electronico', [
                       validators.InputRequired(message='Este campo es obligatorio')])
    
    telefono = IntegerField('Número de telefono o celular', [
                            validators.InputRequired(message='Este campo es obligatorio')])
    
    direccion = StringField('Dirección', [validators.InputRequired(
        message='Este campo es obligatorio')])

#---------------------------------------------------#
#    Datos Del Formulario De Administradores        #
#---------------------------------------------------#    
class administradores(Form):
    tipo_doc = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Cédula de Extranjería', 'Cédula de Extranjería'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Pasaporte', 'Pasaporte'),
        ('NIT', 'NIT'),
        ('Otros', 'Otros')],)
    
    num_iden = IntegerField('Numero Identificación', [
                            validators.InputRequired(message='Este campo es obligatorio')])

    nombre = StringField('Nombre', [validators.InputRequired(
        message='Este campo es obligatorio')])

    email = EmailField('Correo Electronico', [
                       validators.InputRequired(message='Este campo es obligatorio')])

    password = PasswordField('Password', [validators.InputRequired(
        message='Este campo es obligatorio')])

    cargo = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Administrador', 'Administrador'), ('Co-Abministrador', 'Co-Administrador')])

class edit_administradores(Form):
    tipo_doc = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Cédula de Extranjería', 'Cédula de Extranjería'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Pasaporte', 'Pasaporte'),
        ('NIT', 'NIT'),
        ('Otros', 'Otros')],)
    
    num_iden = IntegerField('Numero Identificación', [
                            validators.InputRequired(message='Este campo es obligatorio')])

    nombre = StringField('Nombre', [validators.InputRequired(
        message='Este campo es obligatorio')])

    email = EmailField('Correo Electronico', [
                       validators.InputRequired(message='Este campo es obligatorio')])

    password = PasswordField('Password')

    cargo = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Administrador', 'Administrador'), ('Co-Abministrador', 'Co-Abministrador')])
 
#---------------------------------------------------#
#        Datos Del Formulario De Documentos         #
#---------------------------------------------------#

class documentos(Form):
    
    db = coneccion_db()    
    cursor = db.cursor()
    sql = '''SELECT * FROM  tipo_certificado'''
    cursor.execute(sql)
    options = [(str(result[0]), str(result[1])) for result in cursor.fetchall()]
    tipo_certificado = SelectField('Tipo Certificado', [DataRequired()], choices= options)
    
    tipo_doc_proveedor = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Cédula de Extranjería', 'Cédula de Extranjería'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Pasaporte', 'Pasaporte'),
        ('NIT', 'NIT'),
        ('Otros', 'Otros')])

    num_iden_proveedor = IntegerField('Numero Identificación', [
                            validators.InputRequired(message='Este campo es obligatorio')])

    nombre_razonsocial = StringField('Nombre', [validators.InputRequired(
        message='Este campo es obligatorio')])

    email = EmailField('Correo Electronico', [
                       validators.InputRequired(message='Este campo es obligatorio')])

    current_year = date.today().year
    years = [(str(y), str(y)) for y in range(2020, current_year + 1)]
    years = years[::-1]
    year = SelectField('Año de expedición de documento', [DataRequired()], choices=years)

    archivo = FileField('Nombre Del Archivo', [
                        validators.InputRequired(message='Este campo es obligatorio')])

class edit_documentos(Form):
    
    db = coneccion_db()    
    cursor = db.cursor()
    sql = '''SELECT * FROM  tipo_certificado'''
    cursor.execute(sql)
    options = [(str(result[0]), str(result[1])) for result in cursor.fetchall()]
    tipo_certificado = SelectField('Tipo Certificado', [DataRequired()], choices= options)
    
    tipo_doc_proveedor = SelectField('Tipo De Documento', [DataRequired()], choices=[
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Cédula de Extranjería', 'Cédula de Extranjería'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Pasaporte', 'Pasaporte'),
        ('NIT', 'NIT'),
        ('Otros', 'Otros')])

    num_iden_proveedor = IntegerField('Numero Identificación', [
                            validators.InputRequired(message='Este campo es obligatorio')])

    nombre_razonsocial = StringField('Nombre', [validators.InputRequired(
        message='Este campo es obligatorio')])

    email = EmailField('Correo Electronico', [
                       validators.InputRequired(message='Este campo es obligatorio')])

    current_year = date.today().year
    years = [(str(y), str(y)) for y in range(2020, current_year + 1)]
    years = years[::-1]
    year = SelectField('Año de expedición de documento', [DataRequired()], choices=years)

    archivo = FileField('Nombre Del Archivo')
    
class tip_cert(Form):
    
    tipo_cert   =   StringField('Tipo Certificado', [validators.InputRequired(
        message='Este Campo Es Obligatorio'
    )])