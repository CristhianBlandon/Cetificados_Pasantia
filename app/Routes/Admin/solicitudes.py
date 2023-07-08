from flask import Blueprint, render_template, json
from config import Config
from ...Database import coneccion_db
from ...Helpers.login_requiered import login_required, wraps

solicitudes =   Blueprint('solicitudes', __name__)

@solicitudes.route('/')
#@login_required
def index():
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    sql = ''' SELECT * FROM solicitudes  '''
    
    cursor.execute(sql)
    
    return render_template('Admin/solicitudes.html', datos=cursor)