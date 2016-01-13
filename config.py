# DEBUG has to be to False in a production enrironment for security reasons
DEBUG = True
# BitGo wallet token for IP XX.XXX.XX, dispense an access token at www.bitgo.com and set it here
ACCESS_TOKEN = ''
# Secret key for generating tokens
SECRET_KEY = 'houdini'
# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'password')
# Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'masonicgit.21'
MAIL_PASSWORD = '21.co/learn'
ADMINS = ['masonicgit.21@gmail.com']
# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

# Marketplace settings
MARKET_DATA = [{'name': 'quote',
                'prettyName': 'Profound Quote',
                'url': 'http://10.244.190.107:5000/quote',
                'price': '10'}]
