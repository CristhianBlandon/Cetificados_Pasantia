from flask import Blueprint, render_template, request, jsonify
from flask_bcrypt import Bcrypt
from ...Database import coneccion_db
import forms
from ...Helpers.login_requiered import login_required, wraps

usuarios   = Blueprint('usuarios', __name__)
bcrypt = Bcrypt()

@usuarios.route('/')
#@login_required
def index():
    
    form_admin = forms.administradores()
    
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = ''' SELECT * FROM administradores '''
    cursor.execute(sql)

    return render_template('Admin/usuarios.html', datos=cursor, form_administrador=form_admin)

#---------------------------------------------------#
#        Guardar Datos De Administradores           #
# ---------------------------------------------------#


@usuarios.route('/agregar', methods=['POST', 'GET'])
#@login_required
def admin_administradores_guardar():
    form_admin = forms.administradores(request.form)
    url = '/admin/usuarios'
    
    db  = coneccion_db()
    cursor  = db.cursor()

    if request.method == 'POST':

        tipo_doc = form_admin.tipo_doc.data
        num_doc = form_admin.num_iden.data
        nombre = form_admin.nombre.data
        correo = form_admin.email.data
        contra = form_admin.password.data
        password = bcrypt.generate_password_hash(contra)
        cargo = form_admin.cargo.data

        sql = '''INSERT INTO administradores(Tipo_Doc, Num_Doc, Nombre, Email, Password, Cargo) 
        VALUES(%s, %s, %s, %s, %s, %s)'''
        val = [tipo_doc, num_doc, nombre, correo, password, cargo]

        cursor.execute(sql, val)
        db.commit()

        msg = 'Los datos del usuario has sido guardados correctamente'    
        estado  =   'Correcto'

        return jsonify({'url': url,
                    'msg': msg,
                    'estado': estado})

    else:

        msg = 'Los datos del usuario no han sido guardados.'    
        estado  =   'Error'

        return jsonify({'url': url,
                    'msg': msg,
                    'estado': estado})

# ---------------------------------------------------#
#   Editar Y actualizar Datos De Administradores    #
# ---------------------------------------------------#


@usuarios.route('/editar/<string:id>', methods=['POST', 'GET'])
#@login_required
def admin_administradores_editar(id):

    form_admin = forms.edit_administradores()
    db  = coneccion_db()
    cursor  = db.cursor()

    sql = ''' SELECT * FROM administradores WHERE Num_Doc = {0} '''.format(id)
    cursor.execute(sql)
    data = cursor.fetchall()
    form_admin.tipo_doc.data = data[0][0]
    form_admin.cargo.data = data[0][5]

    return render_template('Admin/Archive/edit_usuarios.html', edita=data[0], form_administrador=form_admin)


@usuarios.route('/actualizar/<string:id>', methods=['POST', 'GET'])
#@login_required
def admin_administradores_actualizar(id):
    form_admin = forms.edit_administradores(request.form)
    db  = coneccion_db()
    cursor  = db.cursor()
    
    url = '/admin/usuarios'

    if request.method == 'POST':

        tipo_doc = form_admin.tipo_doc.data
        num_doc = form_admin.num_iden.data
        nombre = form_admin.nombre.data
        correo = form_admin.email.data
        contra = form_admin.password.data
        cargo = form_admin.cargo.data

        if contra == '':

            sql = '''UPDATE administradores SET Tipo_Doc = %s, Num_Doc = %s,
                    Nombre = %s, Email = %s, Cargo = %s
                    WHERE Num_Doc = %s'''
            val = [tipo_doc, num_doc, nombre, correo, cargo, id]

            cursor.execute(sql, val)
            db.commit()

            
            msg = 'Los datos del usuario han sido actualizados correctamente.'    
            estado  =   'Correcto'

            return jsonify({'url': url,
                    'msg': msg,
                    'estado': estado})

        else:
            password = bcrypt.generate_password_hash(contra)

            sql = '''UPDATE administradores SET Tipo_Doc = %s, Num_Doc = %s,
                    Nombre = %s, Email = %s, Password = %s, Cargo = %s
                    WHERE Num_Doc = %s'''
            val = [tipo_doc, num_doc, nombre, correo, password, cargo, id]

            cursor.execute(sql, val)
            db.commit()
            
            msg = 'Los datos del usuario han sido actualizados correctamente.'   
            estado  =   'Correcto'

            return jsonify({'url': url,
                    'msg': msg,
                    'estado': estado})

    else:
        
        msg = 'Los datos del usuario no se pudieron actualizar.'    
        estado  =   'Error'

        return jsonify({'url': url,
                    'msg': msg,
                    'estado': estado})

# ---------------------------------------------------#
#        Eliminar Datos De Administradores          #
# ---------------------------------------------------#


@usuarios.route('/eliminar/<string:id>')
#@login_required
def admin_administradores_eliminar(id):
    db  = coneccion_db()
    cursor  = db.cursor()
    
    sql = ''' DELETE FROM administradores WHERE Num_Doc = {0} '''.format(id)
    cursor.execute(sql)
    db.commit()

    url = '/admin/usuarios'
    msg = 'Los datos del usuario has sido eliminados correctamente'    
    estado  =   'Correcto'

    return jsonify({'url': url,
                    'msg': msg,
                    'estado': estado})