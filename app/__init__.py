from flask import Flask
import sys, requests, json, urllib.request, os

import sys

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('config')

# Check wallet status with BitGo
token = app.config['ACCESS_TOKEN']

# check for --bitgo-express flag
# should use a real command line argument parser if we add more
if (len(sys.argv) > 1 and sys.argv[1] == '--bitgo-express'):
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
from two1.wallet import Wallet
from two1.server.machine_auth_wallet import MachineAuthWallet
from two1.server import rest_client
from two1.commands.config import Config
from two1 import TWO1_HOST

wallet = Wallet()
host = TWO1_HOST
conf = Config()
username = Config().username
client = rest_client.TwentyOneRestClient(host, MachineAuthWallet(wallet), username)
admin = Admin(app, name='Admin', template_mode='bootstrap3')

class DashboardView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def dashboard(self):
        flush_message = ""
        status_mining = status.status_mining(client)

        if request.method == 'POST':
            print(request.form)
            if request.form['submit'] == 'Flush Earnings':
                flush_message = self.doFlush()
            else:
                if status_mining['is_mining'] == 'A 21 mining chip running (/run/minerd.pid)':
                    os.system('sudo minerd --stop')
                else:
                    os.system('21 mine')

        status_mining = status.status_mining(client)

        if status_mining['is_mining'] == 'A 21 mining chip running (/run/minerd.pid)':
            mine_button_message = 'Click to Stop Miner'
            mining_message = 'Miner Is Running'
        else:
            mine_button_message = 'Click to Start Miner'
            mining_message = 'Miner Is Not Running'

        status_wallet = status.status_wallet(client, wallet)
        status_account = status.status_account(client, wallet)
        status_earnings = client.get_earnings()

        return self.render('admin/dashboard.html', status_mining=status_mining, mining_message=mining_message, status_wallet=status_wallet['wallet'], status_account=status_account, status_earnings=status_earnings, flush_message=flush_message, mine_button_message=mine_button_message)

    def doFlush(self):
        pre_flush_wallet = status.status_wallet(client, wallet)
        flush_response = flush._flush(conf, client)
        print(flush_response)
        status_wallet = status.status_wallet(client, wallet)
        if pre_flush_wallet['wallet']['twentyone_balance'] != status_wallet['wallet']['twentyone_balance']:
            return "Flush successful!"
        else:
            return "Flush error or less than 20000 OffChain Satoshis"


class BlockView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def blockinfo(self):
        doc = urllib.request.urlopen('https://bitcoin.toshi.io/api/v0/blocks/latest')
        content = doc.read()
        raw_data = json.loads(content.decode())
        b_time = raw_data['time']
        b_time = b_time.replace("T", " ")
        b_time = b_time.replace("Z", " UTC")
        return self.render('admin/blockinfo.html', b_height=raw_data['height'], b_hash=raw_data['hash'], b_size=raw_data['size'], b_fees=raw_data['fees'], t_number=raw_data['transactions_count'], b_time=b_time)

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
admin.add_view(BlockView(name='Latest Block Info', endpoint='blockinfo'))
