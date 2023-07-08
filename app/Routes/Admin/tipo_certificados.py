from flask import Blueprint, render_template, request, jsonify
from config import Config
from ...Database import coneccion_db
import forms
import mysql.connector
from ...Helpers.login_requiered import login_required, wraps

tipo_certificados =   Blueprint('tipo_certificados', __name__)

@tipo_certificados.route('/')
#@login_required
def index():
    
    from_tip_Cert = forms.tip_cert()
    
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = ''' SELECT * FROM tipo_certificado '''
    cursor.execute(sql)

    return render_template('Admin/tipo_certificados.html', datos=cursor, formulario_tip_cert=from_tip_Cert)

# ---------------------------------------------------#
#        Crear Nuevo Tipo De Certificado             #
# ---------------------------------------------------#

@tipo_certificados.route('/agregar', methods=['POST', 'GET'])
#@login_required
def agregar():
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    form_tip_cert = forms.tip_cert(request.form)
    url = '/admin/tipo_certificados'
    
    if request.method == 'POST':
        
        tipo_cert = form_tip_cert.tipo_cert.data

        sql = '''INSERT INTO tipo_certificado(Nombre_Certificado, Fecha)
                        VALUES(%s, CURRENT_TIMESTAMP)'''
        val = [tipo_cert]
        cursor.execute(sql, val)
        db.commit()
            
                    
        msg = 'El tipo de certificado, se ha guardado correctamente'
        estado = 'Correcto'
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
#      Editar Y actualizar Tipos de Certificados     #
# ---------------------------------------------------#
        
@tipo_certificados.route('/editar/<string:id>', methods=['POST', 'GET'])
#@login_required
def editar(id):
    
    from_tip_Cert = forms.tip_cert()
    
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = ''' SELECT * FROM tipo_certificado WHERE Tipo_CErtificado = %s'''
    val =   [id]
    cursor.execute(sql,val)
    
    data = cursor.fetchall()

    return render_template('Admin/Archive/edit_tipo_certificados.html', edita=data[0], formulario_tip_cert=from_tip_Cert)
    
    

@tipo_certificados.route('/actualizar/<string:id>', methods=['POST', 'GET'])   
#@login_required
def actualizar(id):
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    form_tip_cert = forms.tip_cert(request.form)
    url = '/admin/tipo_certificados'
    
    if request.method == 'POST':
        
        nombre_tip  =   form_tip_cert.tipo_cert.data
        
        sql =   '''UPDATE tipo_certificado SET Nombre_Certificado = %s, Fecha = CURRENT_TIMESTAMP
                    WHERE Tipo_Certificado = %s'''
        val =   [nombre_tip, id]
        cursor.execute(sql, val)
        db.commit()
        
        msg = 'La actualización del tipo de certificado fue exitosa.'
        estado = 'Correcto'
        return jsonify({'url': url,
                        'msg': msg,
                        'estado': estado})
    else:
        msg = 'No se puedo actualizar el tipo certificado'
        estado = 'Error'
        return jsonify({'url': url,
                        'msg': msg,
                        'estado': estado})
        
# ---------------------------------------------------#
#           Eliminar Tipos De Certificados           #
# ---------------------------------------------------#

@tipo_certificados.route('/eliminar/<string:id>', methods=['POST', 'GET'])   
#@login_required
def eliminar(id):
    
    url = '/admin/tipo_certificados'   
     
    try:
        db = coneccion_db()
        cursor = db.cursor()
        sql = ''' DELETE FROM tipo_certificado WHERE Tipo_Certificado = %s'''
        val = [id]
        cursor.execute(sql, val)
        db.commit()
        msg = 'Se eliminó correctamente el tipo de certificado'
        estado= 'Correcto'
        return jsonify({'url': url, 
                        'msg': msg,
                        'estado': estado})
    
    except mysql.connector.IntegrityError:
        msg = 'No se puede eliminar el tipo certificado porque tiene documentos asociados'
        estado = 'Error'
        return jsonify({'url': url,
                        'msg': msg,
                        'estado': estado})

