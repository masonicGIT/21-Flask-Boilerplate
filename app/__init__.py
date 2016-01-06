from flask import Flask
import sys, requests, json

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

# Setup the dashboard
from two1.commands import status
from two1.commands import log
from two1.commands import flush
from two1.commands import mine
from two1.lib.server import rest_client
from two1.commands.config import Config
from two1.commands.config import TWO1_HOST

conf = Config()
host = TWO1_HOST
client = rest_client.TwentyOneRestClient(host, conf.machine_auth, conf.username)
admin = Admin(app, name='Admin', template_mode='bootstrap3')

class DashboardView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def dashboard(self):
        flush_message = ""
        if request.method == 'POST':
            flush_message = self.doFlush(self)
        status_mining = status.status_mining(conf, client)
        status_wallet = status.status_wallet(conf, client)
        status_account = status.status_account(conf)
        status_earnings = client.get_earnings()
        print(status_earnings)
        return self.render('admin/dashboard.html', status_mining=status_mining, status_wallet=status_wallet['wallet'], status_account=status_account, status_earnings=status_earnings, flush_message=flush_message)
    
    def doFlush(self):
        pre_flush_wallet = status.status_wallet(conf, client)
        flush_response = flush.flush_earnings(conf, client)
        print(flush_response)
        status_wallet = status.status_wallet(conf, client)
        if pre_flush_wallet['wallet']['twentyone_balance'] != status_wallet['wallet']['twentyone_balance']:
            return "Flush successful!"
        else:
            return "Flush error or less than 20000 OffChain Satoshis"


class ModelView(ModelView):

    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response('You have to an administrator.', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True

# Users
admin.add_view(ModelView(User, db.session))
admin.add_view(DashboardView(name='Dashboard', endpoint='dashboard'))
