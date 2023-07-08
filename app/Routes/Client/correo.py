from flask import Blueprint, json, url_for, jsonify, render_template,request, session
from config import Config
from ...Database import coneccion_db
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import datetime
import forms
import smtplib
import ssl
import requests

email   = Blueprint('email', __name__)

@email.route('/datos', methods=['POST'])
def validacion():
    datos_email = forms.email(request.form)
    
    db  = coneccion_db()
    cursor  = db.cursor()
    
    url = ''

    if (request.method == 'POST'):
        recaptcha = request.form['g-recaptcha-response']
            
        if is_human(recaptcha):
            tipo_doc = datos_email.tipo_doc.data
            num_iden = datos_email.num_iden.data
            tip_cert = datos_email.tipo_certificado.data
            year = datos_email.year.data

            try:
                sql = ''' SELECT * FROM documentos WHERE Tipo_Doc = %s AND Num_Proveedor = %s AND Tipo_Certificado = %s AND Year = %s '''
                val = [tipo_doc, num_iden, tip_cert, year]
                cursor.execute(sql, val)
                resultados = cursor.fetchall()

                if resultados is not None:
                    correo = envio_email(resultados)
                    correo_estado = correo[0]
                    correo_msg = correo[1]                    
                    return jsonify({'url': url,
                                    'msg': correo_msg,
                                    'estado': correo_estado})
                
            except:
                msg = '''No se pudo completar la solicitud, por favor verifique que los datos ingresados esten correctos.'''
                estado = 'Error'
                return jsonify({'url': url,
                                'msg': msg,
                                'estado': estado})

        else:
            msg = '''No se puedo completar la solicitud por error en el Recaptcha, 
                por favor verificarse con el Rcaptcha'''
            estado= 'Error'
            return jsonify({'url': url,
                            'msg': msg,
                            'estado': estado})

    else:
            msg = '''No se puedo completar la solicitud por error en el Formulario, 
                por favor intentarlo más tarde, si el error continua comuniquese con atención al cliente'''
            estado= 'Error'
            return jsonify({'url': url,
                            'msg': msg,
                            'estado': estado})

def envio_email(consulta):
    db  = coneccion_db()
    cursor  = db.cursor()

    if consulta != None:
        for ext in consulta:
            resultado_con = ext

        id_cer = resultado_con[0]
        tipo_doc = resultado_con[1]
        num_pro = resultado_con[2]
        nombre = resultado_con[3]
        certificado = resultado_con[6]
        solicitud_certi = resultado_con[8]

        session['tipo_doc'] = tipo_doc
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # year = resultado_con[5]

        ruta_certificado = Config.UPLOAD_FOLDER + '/('+ str(id_cer) +',)' + certificado

        sql = 'SELECT Email, Num_Solicitudes FROM proveedores WHERE Tipo_Doc = %s AND Num_Proveedor = %s'
        val = [resultado_con[1], resultado_con[2]]
        cursor.execute(sql, val)
        busqueda = cursor.fetchall()

        for ext in busqueda:
            resultado_bus = ext

        sender = Config.MAIL_USERNAME
        receiver = resultado_bus[0]
        asunto = 'Certificado UGCA'
        
        body = render_template('Clients/correo.html', tip=tipo_doc, num=num_pro,
                                nom=nombre, fecha=fecha_actual)
        
        sql = '''INSERT INTO solicitudes(Tipo_Doc, Num_Proveedor, Nombre_RazonSocial, Email, Id_Documento, Documento, Fecha)
                    VALUES(%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP )
                    '''
        datos = [tipo_doc, num_pro, nombre, resultado_bus[0], id_cer, certificado]
        cursor.execute(sql, datos)
        
        soli_proveedor = solicitud_proveedor(tipo_doc, num_pro, resultado_bus[1])

        if soli_proveedor != None:
            soli_certi = solicitud_certificado(id_cer, solicitud_certi)

            if soli_certi != None:

                msg = MIMEMultipart()

                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = asunto
                msg.attach(MIMEText(body, 'html', 'utf-8'))

                pdfApart = MIMEApplication(open(ruta_certificado, 'rb').read())
                pdfApart.add_header('Content-Disposition',
                            'attachment', filename=certificado)

                msg.attach(pdfApart)
                text = msg.as_string()

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(sender, password= Config.MAIL_PASSWORD)
                    enviados = server.sendmail(sender, receiver, text)

                if enviados:
                    # Hay errores al enviar el correo
                    estado = 'Error'
                    msg = 'No se pudo eniar el certificado, por favor intentarlo mas tarde'
                    return estado, msg

                else:

                    correo = str(resultado_bus[0])
                    nombre_usuario, dominio = correo.split('@')
                    nombre_usuario_procesado = nombre_usuario[:3] + '*' * (len(nombre_usuario) - 3)
                    dominio_procesado = dominio[:3] + '*' * (len(dominio) - 3)
                    correo_procesado = nombre_usuario_procesado + '@' + dominio_procesado

                    estado = 'Enviado'
                    msg = 'El certificado a sido enviado a su correo: ' + correo_procesado
                    return estado, msg
                
            else:
                estado = 'Error'
                msg = 'No se pudo enviar el certificado, por error de envio de correo, por favor intentarlo más tarde muchas gracias'
                return estado, msg

        else:
            estado = 'Error'
            msg = 'No se pudo eniar el certificado, por error de datos del certificado, por favor intentarlo más tarde muchas gracias'
            return estado, msg

    else:
        estado= 'Error'
        msg = 'No se pudo eniar el certificado, por error de datos del proveedor, por favor intentarlo más tarde muchas gracias'

        return estado, msg

def solicitud_proveedor(tipo_doc, num_pro, solicitud):
    db  = coneccion_db()
    cursor  = db.cursor()

    can_soli = solicitud + 1
    sql = ''' UPDATE proveedores SET Num_Solicitudes = %s WHERE Tipo_Doc = %s AND Num_Proveedor = %s'''
    val = [can_soli, tipo_doc, num_pro]
    cursor.execute(sql, val)
    db.commit()

    validacion_act = cursor.rowcount

    if validacion_act > 0:
        estado = 'Correcto'
        return estado
    
    else:
        return None

def solicitud_certificado(id_certi, solicitud):
    db  = coneccion_db()
    cursor  = db.cursor()
    
    can_soli = solicitud + 1
    sql = ''' UPDATE documentos SET Num_Solicitudes = %s WHERE Id_Documento = %s'''
    val = [can_soli, id_certi]
    cursor.execute(sql, val)
    db.commit()

    validacion_act = cursor.rowcount

    if validacion_act > 0:
        estado = 'Correcto'
        return estado
    
    else:
        return None


def is_human(captcha_response):
    secret = Config.SECRET_SITEKEY
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']