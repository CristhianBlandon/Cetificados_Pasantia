from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        if user:
            role = session.get('profile')
            if role == "Administrador":
                return f(*args, **kwargs)
            elif role == "Co-Administrador":
                if f.__name__ in ["admin_index",
                                  # Certificados
                                  "admin_documentos", "admin_documentos_guardar",
                                  "admin_documentos_editar", "admin_documentos_actualizar", "admin_certificados_eliminar",
                                  "admin_documentos_buscar_proveedor", "admin_documentos_mostar_proveedor",
                                  # Proveedores
                                  "admin_proveedores", "admin_proveedores_guardar", "admin_proveedores_editar",
                                  "admin_proveedores_actualizar", "admin_proveedores_eliminar",
                                  # Registro
                                  "admin_solicitudes"
                                  ]:
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for("admin_index"))
            elif role == "user" and f.__name__ == "user_view":
                return f(*args, **kwargs)
        return redirect(url_for("admin_login.login"))
    return decorated_function