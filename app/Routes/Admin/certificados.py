from flask import Blueprint, render_template, jsonify, send_from_directory, request
from config import Config
from ...Database import coneccion_db
from werkzeug.utils import secure_filename
from os import remove
from ...Helpers.login_requiered import login_required, wraps

import forms
import os

certificados    =   Blueprint('cerificados', __name__)

@certificados.route('/')
#@login_required
def index():
    
    form_cert = forms.documentos()
    
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = ''' SELECT `Id_Documento`,`Tipo_Doc`,`Num_Proveedor`,`Nombre_RazonSocial`,`Email`, 
                tipo_certificado.Nombre_Certificado,`Documento`,`Year`,`Num_Solicitudes`, documentos.Fecha 
                FROM `documentos`, tipo_certificado
                WHERE documentos.Tipo_Certificado = tipo_certificado.Tipo_Certificado; '''
    cursor.execute(sql)

    return render_template('Admin/certificados.html', datos=cursor, formulario_cert=form_cert)

@certificados.route('/Search_Nombre')
#@login_required
def admin_documentos_buscar_proveedor():

    db  = coneccion_db()
    cursor  = db.cursor()
    
    term = request.args.get('term')
    sql = "SELECT Nombre_RazonSocial FROM proveedores WHERE Nombre_RazonSocial LIKE %s "
    val = ['%' + term + '%']
    cursor.execute(sql, val)
    nombre = [row[0] for row in cursor.fetchall()]
    return jsonify(nombre)


@certificados.route('/Mostar_Nombre')
#@login_required
def admin_documentos_mostar_proveedor():
    db  = coneccion_db()
    cursor  = db.cursor()
    valor = request.args.get('valor')
    sql = '''SELECT Tipo_Doc,Num_Proveedor,Email FROM proveedores WHERE Nombre_RazonSocial = %s'''
    val = [valor]
    cursor.execute(sql, val)
    data = cursor.fetchall()
    return jsonify(data)

# ---------------------------------------------------#
#          Guardar Datos De Certificados             #
# ---------------------------------------------------#

@certificados.route('/agregar', methods=['POST', 'GET'])
#@login_required
def agregar():
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    form_cert = forms.documentos(request.form)
    url = '/admin/certificados'
    
    if request.method == 'POST':
        tipo_doc = form_cert.tipo_doc_proveedor.data
        num_doc = form_cert.num_iden_proveedor.data
        tipo_cert = form_cert.tipo_certificado.data
        year = form_cert.year.data

        datos = validacion_documento(tipo_doc, num_doc, tipo_cert, year)
        
        if datos != None:
            
            nombre = form_cert.nombre_razonsocial.data
            email = form_cert.email.data
            certificado = request.files[form_cert.archivo.name]
            file = secure_filename(certificado.filename)

            sql = '''INSERT INTO documentos(Tipo_Doc, Num_Proveedor, Nombre_RazonSocial, Email, Tipo_Certificado, Documento, Year, Fecha)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)'''
            val = [tipo_doc, num_doc, nombre, email, tipo_cert, file, year]
            cursor.execute(sql, val)
            db.commit()
            
            if cursor.rowcount == 1:
                
                nom_certi = nombre_file(file)

                certificado.save(os.path.join(Config.UPLOAD_FOLDER, nom_certi))
                    
                msg = 'Los datos ingresados, se han guardado correctamente'
                estado = 'Correcto'
                return jsonify({'url': url,
                                'msg': msg,
                                'estado': estado})
            
            else:
                msg = 'Los datos ingresados, no se pudieron registrar ya que no se cumplio con los datos pertinentes.'
                estado = 'Error'
                return jsonify({'url': url,
                                'msg': msg,
                                'estado': estado})
                
        
        else:
            msg = 'Los datos ingresados, ya se encuentran registrados.'
            estado = 'Error'
            return jsonify({'url': url,
                            'msg': msg,
                            'estado': estado})
        
    else:
        msg = 'No se resivido ningun tipo de datos'
        estado = 'Error'
        return jsonify({'url': url,
                        'msg': msg,
                        'estado': estado})
        
# ---------------------------------------------------#
#                Mostrar Documentos                  #
# ---------------------------------------------------#

@certificados.route('/vista/<string:id>/<string:file>')
#@login_required
def admin_get_file(id, file):
    # Busqueda del archivo por el nombre // File search by name
    name = '(' + id + ',)' + file
    ruta = Config.UPLOAD_FOLDER + '/' 
    archivo = send_from_directory(ruta, name)

    return archivo

# ---------------------------------------------------#
#     Editar Y actualizar Datos De Documentos        #
# ---------------------------------------------------#

@certificados.route('/editar/<string:id>', methods=['POST', 'GET'])
#@login_required
def admin_documentos_editar(id):
    
    form_cert = forms.edit_documentos()
    
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = ''' SELECT `Id_Documento`,`Tipo_Doc`,`Num_Proveedor`, `Nombre_RazonSocial`, `Email`, 
    `Documento`,`Year`,tipo_certificado.Tipo_Certificado ,tipo_certificado.Nombre_Certificado FROM `documentos`, tipo_certificado 
    WHERE `Id_Documento` = {0}
    AND tipo_certificado.Tipo_Certificado = documentos.Tipo_Certificado '''.format(id)
    cursor.execute(sql)
    data = cursor.fetchall()
    form_cert.tipo_doc_proveedor.data = data[0][1]
    form_cert.tipo_certificado.data = str(data[0][7])
    form_cert.year.data = str(data[0][6])

    return render_template('Admin/Archive/edit_certificados.html', edita=data[0], formulario_cert=form_cert)

@certificados.route('/actualizar/<string:id>/<string:carpeta>/<string:name>', methods=['POST', 'GET'])
#@login_required
def admin_documentos_actualizar(id, carpeta, name):

    form_cert = forms.edit_documentos(request.form)
    url = '/admin/certificados'
    
    db  = coneccion_db()
    cursor  = db.cursor()

    if request.method == 'POST':

        tipo_doc = form_cert.tipo_doc_proveedor.data
        ident = form_cert.num_iden_proveedor.data
        nombre = form_cert.nombre_razonsocial.data
        email = form_cert.email.data
        tipo_cert = form_cert.tipo_certificado.data
        f = request.files[form_cert.archivo.name]
        file = secure_filename(f.filename)
        year = form_cert.year.data
            
        if file == '':

            sql = ''' UPDATE documentos SET Tipo_Doc =%s, Num_Proveedor = %s, Nombre_RazonSocial = %s,
                    Email = %s,  Year = %s, Tipo_Certificado = %s, Fecha = CURRENT_TIMESTAMP WHERE Id_Documento = %s'''
            val = [tipo_doc, ident, nombre, email, year, tipo_cert, id]
            cursor.execute(sql, val)
            db.commit()

            msg = 'Los datos ingresados, se han guardado correctamente'
            estado = 'Correcto'                    
            return jsonify({'url': url,
                            'msg': msg,
                            'estado': estado})

        else:

            sql = ''' UPDATE documentos SET Tipo_Doc =%s, Num_Proveedor = %s, Nombre_RazonSocial = %s,
            Email = %s, Documento = %s, Year = %s, Tipo_Certificado = %s, Fecha = CURRENT_TIMESTAMP WHERE Id_Documento = %s'''
            val = [tipo_doc, ident, nombre, email, file, year, tipo_cert, id]
            cursor.execute(sql, val)
            db.commit()

            nom_delet = '(' + str(id)+',)'+name
            filename_ext = '(' + str(id)+',)'+file

            remove(os.path.join(Config.UPLOAD_FOLDER, nom_delet))
            f.save(os.path.join(Config.UPLOAD_FOLDER, filename_ext))
            

            msg = 'Los datos ingresados, se han guardado correctamente'
            estado = 'Correcto'                    
            return jsonify({'url': url,
                                'msg': msg,
                                'estado': estado})
            
# ---------------------------------------------------#
#           Eliminar Datos De Documentos             #
# ---------------------------------------------------#

@certificados.route('/eliminar/<string:id>/<string:certificado>')
#@login_required
def eliminacion_datos(id, certificado):
    
    url = '/admin/certificados'
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    nom_delet ='(' + str(id)+',)' + certificado
    
    sql = ''' DELETE FROM documentos WHERE Id_Documento = %s '''
    val =   [id]
    cursor.execute(sql, val)
    
    # Eliminacion del archivo // Delete the file
    remove(os.path.join(Config.UPLOAD_FOLDER, nom_delet))
    
    msg = 'El certificado y los datos fueron eliminados correctamente'
    estado = 'Correcto'                    
    return jsonify({'url': url,
                    'msg': msg,
                    'estado': estado})


# ---------------------------------------------------#
#           Funciones Extras En Validacion           #
# ---------------------------------------------------#

def validacion_documento(tipo_doc, num_doc, tipo_cert, year):
    
    db  = coneccion_db()
    cursor  = db.cursor()
    sql = '''SELECT Tipo_Doc, Num_Proveedor, Tipo_Certificado, Year FROM documentos WHERE Tipo_Doc = %s AND Num_Proveedor = %s AND Tipo_Certificado = %s AND Year = %s'''
    val = [tipo_doc, num_doc, tipo_cert, year]
    cursor.execute(sql, val)    
    
    resultado = cursor.fetchone()
            
    # Aseguararse que los datos sean diferentes a None // Make sure the data is different from None
    if resultado != None:
        return None
    
    # de lo contrario es igual a ninguno // else otherwise equals none
    else:
        # Datos a reenviar para el registro //  Data to send for registration
        return 'Registrar'
    
def nom_carp(tipo_cert):
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    sql = ''' SELECT  Nombre_Certificado FROM tipo_certificado WHERE tipo_certificado = %s'''
    val = [tipo_cert]
    cursor.execute(sql, val)    
    carpeta = cursor.fetchone()
    
    for ext in carpeta:
        return ext
    
def nombre_file(file):
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    sql = '''SELECT MAX(Id_Documento) FROM documentos'''
    cursor.execute(sql)
    
    id = cursor.fetchall()
            
    for ext in id:
        file_name = str(ext) + file
        return file_name
    
def validacion_tipo(tipo_certificado, carpeta):
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    sql = '''SELECT Nombre_Certificado FROM tipo_certificado WHERE Tipo_Certificado = %s'''
    val =   [tipo_certificado]
    cursor.execute(sql, val)
    
    datos = cursor.fetchone()
    
    for ext in datos:
        return ext