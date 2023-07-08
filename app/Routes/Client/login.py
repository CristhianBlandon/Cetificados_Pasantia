from authlib.integrations.flask_client import OAuth
from config import Config
from ...Database import coneccion_db
from flask import (Blueprint, Flask,
                   render_template, url_for, redirect,
                   session, request)
from flask_bcrypt import Bcrypt

from ...Helpers.oauth_login import oauth, microsoft

import forms

admin_login   =   Blueprint('admin_login', __name__)
bcrypt =   Bcrypt()

@admin_login.route('/')
def login():
    form_login = forms.login()
    return render_template('Clients/login.html', formulario = form_login)

# **********************************************************************#
#                              Login Servidor                          #
# **********************************************************************#


@admin_login.route('/local', methods=['POST', 'GET'])
def admin_login_local():
    login_form = forms.login(request.form)
    db  = coneccion_db()
    cursor  = db.cursor()
    
    if request.method == 'POST':
        email = login_form.email.data
        passw = login_form.password.data
        vali_email = local_email(email)

        if vali_email == True:
            sql = '''SELECT Nombre, Email, Password, Cargo FROM administradores WHERE Email = %s'''
            val = [email]
            cursor.execute(sql, val)
            result = cursor.fetchone()

            if result:
                if bcrypt.check_password_hash(result[2], passw):
                    session['picture'] = 'img/perfil/escudo_admin.png'
                    session['name'] = result[0]
                    session['email'] = result[1]
                    session['profile'] = result[3]
                    return redirect(url_for("admin_index.index"))

                else:
                    return redirect(url_for("admin_login.login"))

            else:
                return redirect(url_for("admin_login.login"))
        else:
            return redirect(url_for("admin_login.login"))


def local_email(email):
    db  = coneccion_db()
    cursor  = db.cursor()
    
    sql = '''SELECT Email FROM administradores WHERE Email = %s '''
    val = [email]
    cursor.execute(sql, val)
    result = cursor.fetchall()
    correo = True
    if result == '':
        return redirect(url_for("login"))
    else:
        return correo

# **********************************************************************#
#                        Login Google                                  #
# **********************************************************************#

@admin_login.route('/google',methods = ['POST', 'GET'])
def login_google():
    google = oauth.create_client('google')
    redirect_uri = url_for('admin_login.authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)


@admin_login.route('/authorize/google')
def authorize_google():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user = resp.json()
    user = oauth.google.userinfo()
    dominio = Config.DOMINIO_GOOGLE_CORREO
    session['dominio'] = dominio
    session['email'] = user['email']
    session['name'] = user['name']
    session['picture'] = user['picture']
    user_va = validacion_correos(session['email'], dominio)

    if not user_va:
        return redirect(url_for("admin_login.login"))

    else:
        session['profile'] = user_va[1]
        return redirect(url_for("admin_index.index"))

# **********************************************************************#
#                             Login Outlook                             #
# **********************************************************************#

@admin_login.route('/microsoft')
def login_microsoft():
    redirect_uri = url_for('admin_login.authorize_microsoft', _external=True)
    return microsoft.authorize_redirect(redirect_uri)

@admin_login.route('/authorize/microsoft')
def authorize_microsoft():
    token = microsoft.authorize_access_token()
    resp = microsoft.get('me', token=token)
    user = resp.json()
    session['email'] = user['userPrincipalName']
    session['name'] = user['displayName']
    dominio = Config.DOMINIO_MICROSOFT_CORREO
    user_va = validacion_correos(session['email'], dominio)

    if not user_va:
        return redirect(url_for("admin_login.login"))

    else:
        session['picture'] = 'img/perfil/escudo_admin.png'
        session['dominio'] = dominio
        session['profile'] = user_va[1]
        return redirect(url_for("admin_index.index"))
    
# **********************************************************************#
#                        Validacion De Correos                         #
# **********************************************************************#

def validacion_correos(email, dominio):
    db  = coneccion_db()
    cursor  = db.cursor()

    if dominio == 'Google':

        sql = '''SELECT Email, Cargo FROM administradores WHERE Email = %s'''
        val = [email]
        cursor.execute(sql, val)

        # Valirable que almacena los datos traidos por la consulta // Valirable that stores the data fetched by the query
        id_file = cursor.fetchall()
        for ext in id_file:
            return ext

    elif dominio == 'Microsoft':

        sql = '''SELECT Email, Cargo FROM administradores WHERE Email = %s'''
        val = [email]
        cursor.execute(sql, val)

        # Valirable que almacena los datos traidos por la consulta // Valirable that stores the data fetched by the query
        id_file = cursor.fetchall()
        for ext in id_file:
            return ext