from flask import Flask
import sys, requests, json, urllib.request, os

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('config')

# Check wallet status with BitGo
token = app.config['ACCESS_TOKEN']

try:
    r = requests.get('http://localhost:3080/api/v1/user/session', headers = {'Authorization': 'Bearer ' + token,'Content-Type': 'application/json'}, data={})
    if (r.status_code == 404):
        print('Your BitGo Express access token has expired or is invalid for this IP address')
        print('You may acquire a new one at https://www.bitgo.com')
        print('The in-app wallet will remain inactive until a new access token is set')
    if (r.status_code == 200):
        print('BitGo Express running...')

except:
    print('BitGo Express is not currently running on your machine')
    print('To enable the in-app wallet please navigate to goo.gl/AaU8Rp for installation instructions')
    print('and set your token in config.py')

# Setup the database
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the mail server
from flask.ext.mail import Mail
mail = Mail(app)

# Setup the password crypting
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import the views
from app.views import main, user, error
app.register_blueprint(user.userbp)

# Setup the user login process
from flask.ext.login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()

# Setup the admin interface
from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask_admin import Admin, expose, BaseView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import LoginManager
from flask.ext.admin.contrib.fileadmin import FileAdmin

