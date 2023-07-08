from flask import Blueprint, render_template, json
from config import Config
from ...Helpers.login_requiered import login_required, wraps

admin_index =   Blueprint('admin_index', __name__)

@admin_index.route('/')
#@login_required
def index():
    return render_template('Admin/index.html')