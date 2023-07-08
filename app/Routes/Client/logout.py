from config import Config
from flask import (Blueprint,
                   url_for, redirect,
                   session)

admin_logout   =   Blueprint('admin_logout', __name__)

@admin_logout.route('/')
def logout():
    if session.get('dominio') == Config.DOMINIO_MICROSOFT_CORREO:

        for key in list(session.keys()):
            session.pop(key)
        return redirect(url_for("admin_login.login"))

    else:
        for key in list(session.keys()):
            session.pop(key)
        return redirect(url_for("admin_login.login"))