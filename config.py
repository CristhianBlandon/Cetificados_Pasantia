from dotenv import load_dotenv
from datetime import timedelta

import os

load_dotenv()

class Config:
    
    SECRET_KEY_API  =   os.getenv('SECRET_KEY_API')
    
    UPLOAD_FOLDER   =   'E:/certificados/app/Uploads' 
    #'C:/Users/requisitoinformatica/Documents/python flask/certificados/app/Uploads/'
    
    MYSQL_DB    =   os.getenv('MYSQL_DATABASE')
    MYSQL_HOST  =   os.getenv('MYSQL_HOST')
    MYSQL_USER  =   os.getenv('MYSQL_USER')
    MYSQL_PASS  =   os.getenv('MYSQL_PASSWORD')
    
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET')
    DOMINIO_GOOGLE_CORREO = os.getenv('DOMINIO_GOOGLE_CORREO')
    
    MICROSOFT_CLIENT_ID=os.getenv('MICROSOFT_CLIENT_ID')
    MICROSOFT_CLIENT_SECRET=os.getenv('MICROSOFT_CLIENT_SECRET')
    DOMINIO_MICROSOFT_CORREO = os.getenv('DOMINIO_MICROSOFT_CORREO')
    
    SITEKEY = os.getenv('SITEKEY')
    SECRET_SITEKEY = os.getenv('SECRET_SITEKEY')
        
    FOLDER_TEMPLATE =   'Views/Templates/'
    FOLDER_STATIC   =   'Views/Static/'
    FOLDER_UPLOADS  =   'Uploads'
    
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=45)