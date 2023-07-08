from authlib.integrations.flask_client import OAuth
from config import Config
from flask import Flask 

app = Flask(__name__)
oauth = OAuth(app)
    
google = oauth.register(
    name='google',
    client_id='708121133558-282og19jlbgvvd8aooqfou98hrlr9jtg.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'prompt': 'select_account'},
    api_base_url='https://www.googleapis.com/oauth2/v1/certs',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )
    
microsoft = oauth.register(
    name='microsoft',
    client_id=Config.MICROSOFT_CLIENT_ID,
    client_secret=Config.MICROSOFT_CLIENT_SECRET,
    access_token_url='https://login.microsoftonline.com/organizations/oauth2/v2.0/token',
    access_token_params=None,
    authorize_url='https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize',
    authorize_params={'prompt': 'select_account'},
    api_base_url='https://graph.microsoft.com/v1.0/',
    userinfo_endpoint='https://graph.microsoft.com/v1.0/users',
    client_kwargs={'scope': 'User.Read'},
    )