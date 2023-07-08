from flask import Blueprint, render_template, json
from config import Config
import forms

clientes    =   Blueprint('index', __name__)

@clientes.route('/')
def index():
    form_email = forms.email()
    form_email.tipo_certificado.choices = forms.email.get_tipo_certificado_options()
    sitekey = Config.SITEKEY
    return render_template('Clients/index.html', formulario=form_email, form_recaptcha=sitekey)