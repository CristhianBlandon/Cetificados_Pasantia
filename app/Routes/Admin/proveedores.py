from flask import Blueprint, render_template, jsonify, request
from config import Config
from ...Database import coneccion_db
import mysql.connector
from ...Helpers.login_requiered import login_required, wraps

import forms

proveedores =   Blueprint('proveedores', __name__)

@proveedores.route('/')
#@login_required
def index():
    
    form_prov = forms.proveedores()
    
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = ''' SELECT * FROM proveedores  '''

    cursor.execute(sql)

    return render_template('Admin/proveedores.html', datos=cursor, formulario_prov=form_prov)

# ---------------------------------------------------#
#           Guardar Datos De Proveedores            #
# ---------------------------------------------------#


@proveedores.route('/agregar', methods=['POST', 'GET'])
#@login_required

def admin_proveedores_guardar():

    form_prov = forms.proveedores(request.form)
    url = '/admin/proveedores'
    db  = coneccion_db()
    cursor  = db.cursor()

    if request.method == 'POST':

        tipo_doc = form_prov.tipo_doc.data
        num_doc = form_prov.num_iden.data
        nombre = form_prov.nombre_razonsocial.data
        correo = form_prov.email.data
        telefono = form_prov.telefono.data
        direcion = form_prov.direccion.data

        sql = '''INSERT INTO proveedores(Tipo_Doc, Num_Proveedor, Nombre_RazonSocial, Email, Telefono, Direccion) 
        VALUES(%s, %s, %s, %s, %s, %s)'''

        val = [tipo_doc, num_doc, nombre, correo, telefono, direcion]

        cursor.execute(sql, val)
        db.commit()

        if cursor.rowcount == 1:
            msg = 'Los datos ingresados del proveedor, se han guardado correctamente'
            estado = 'Correcto'
            return jsonify({'url': url,
                            'msg': msg,
                            'estado': estado})
        else:
            msg = 'Los datos ingresados del proveedor, ya se encuentran registrados'
            estado = 'Error'
            return jsonify({'url': url,
                            'msg': msg,
                            'estado': estado})
    else:
        msg = 'Los datos ingresados del proveedor, son errados'
        estado = 'Error'
        return jsonify({'url': url,
                            'msg': msg,
                            'estado': estado})

# ---------------------------------------------------#
#     Editar Y actualizar Datos De Proveedores       #
# ---------------------------------------------------#


@proveedores.route('/editar/<string:doc>/<string:id>', methods=['POST', 'GET'])
#@login_required

def admin_proveedores_editar(doc, id):
    form_prov = forms.proveedores()
    
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = '''SELECT * FROM proveedores WHERE Tipo_Doc = %s AND Num_Proveedor = %s'''
    val = [doc, id]
    cursor.execute(sql, val)
    data = cursor.fetchall()
    form_prov.tipo_doc.data = data[0][0]

    return render_template('Admin/Archive/edit_proveedores.html', formulario_prov=form_prov, edita=data[0])


@proveedores.route('/actualizar/<string:doc>/<string:id>', methods=['POST', 'GET'])
#@login_required

def admin_proveedores_actualizar(doc, id):

    form_prov = forms.proveedores(request.form)
    url = '/admin/proveedores'
    
    db  = coneccion_db()
    cursor  = db.cursor()

    if request.method == 'POST':

        tipo_doc = form_prov.tipo_doc.data
        num_doc = form_prov.num_iden.data
        nombre = form_prov.nombre_razonsocial.data
        correo = form_prov.email.data
        tele = form_prov.telefono.data
        direc = form_prov.direccion.data

        sql = ''' UPDATE proveedores SET Tipo_Doc = %s, Num_Proveedor = %s, 
        Nombre_RazonSocial = %s, Email = %s, Telefono = %s, Direccion = %s 
        WHERE Tipo_Doc = %s AND Num_Proveedor = %s'''
        val = [tipo_doc, num_doc, nombre, correo, tele, direc, doc, id]
        cursor.execute(sql, val)
        db.commit()

        msg = 'Los datos del proveedor se actualizaron correctamente.'
        estado = 'Correcto'
        return jsonify({'url': url,
                        'msg': msg,
                        'estado': estado})
    
    else:
        msg = 'No se puede actualizar el proveedor por datos repetidos que estan guardados.'
        estado = 'Error'
        return jsonify({'url': url,
                        'msg': msg,
                        'estado': estado})

# ---------------------------------------------------#
#           Eliminar Datos De Proveedores           #
# ---------------------------------------------------#


@proveedores.route('/eliminar/<string:doc>/<string:id>')
#@login_required
def admin_proveedores_eliminar(doc, id):
    url = '/admin/proveedores'   
     
    try:
        db = coneccion_db()
        cursor = db.cursor()
        sql = ''' DELETE FROM proveedores WHERE Tipo_Doc = %s AND Num_Proveedor = %s '''
        val = [doc, id]
        cursor.execute(sql, val)
        db.commit()
        msg = 'Se eliminó correctamente los datos del proveedor y sus certificados'
        estado= 'Correcto'
        return jsonify({'url': url, 
                        'msg': msg,
                        'estado': estado})
    
    except mysql.connector.IntegrityError:
        msg = 'No se puede eliminar el proveedor porque tiene documentos asociados'
        estado = 'Error'
        return jsonify({'url': url,
                        'msg': msg,
                        'estado': estado})