from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_wtf import CSRFProtect
from config import Config

from flask_bcrypt import Bcrypt

from .Routes import clientes, email, admin_login, admin_index, certificados, proveedores, solicitudes, tipo_certificados, usuarios, admin_logout

app = Flask(__name__,   static_folder = Config.FOLDER_STATIC, 
                        template_folder = Config.FOLDER_TEMPLATE)
app.config.from_object(Config)

app.secret_key  =   app.config['SECRET_KEY_API']
crsf = CSRFProtect(app)
bcrypt =   Bcrypt()

app.register_blueprint(clientes, url_prefix = '/')
app.register_blueprint(email, url_prefix = '/email')
app.register_blueprint(admin_login, url_prefix = '/login')
app.register_blueprint(admin_logout, url_prefix = '/logout')
app.register_blueprint(admin_index, url_prefix = '/admin')
app.register_blueprint(certificados, url_prefix = '/admin/certificados')
app.register_blueprint(proveedores, url_prefix = '/admin/proveedores')
app.register_blueprint(solicitudes, url_prefix = '/admin/solicitudes')
app.register_blueprint(tipo_certificados, url_prefix = '/admin/tipo_certificados')
app.register_blueprint(usuarios, url_prefix = '/admin/usuarios')