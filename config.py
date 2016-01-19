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

# Bitcoin Tutorials
TUTORIALS = [
{'url': 'gist.github.com/pkrasam/d1aa82d5a70189d8f2ad', 'name': 'gist.01_Build_a_Simple_Bitcoin_Game.md', 'prettyName': 'Build a Simple Bitcoin Game'},
{'url': 'gist.github.com/pkrasam/af4d79d308e1c1cdcce9', 'name': 'gist.02_Bitcoin-payable_HTTP_Proxy.md', 'prettyName': 'Bitcoin-payable HTTP Proxy'},
{'url': 'gist.github.com/pkrasam/afc276cb67dde0abd04c', 'name': 'gist.03_Receive_an_SMS_from_Anyone_for_Bitcoin.md', 'prettyname': 'Receive an SMS from Anyone for Bitcoin'},
{'url': 'gist.github.com/pkrasam/2befdb9c9b692ef12078', 'name': 'gist.04_A Bitcoin-Payable_API.md', 'prettyName': 'A Bitcoin-Payable API'},
{'url': 'gist.github.com/pkrasam/92949b1e9dadf7910bf9', 'name': 'gist.05_A_Bitcoin_Mashup.md', 'prettyName': 'A Bitcoin Mashup'},
{'url': 'gist.github.com/pkrasam/b9b36f897d7d35483599', 'name': 'gist.06_Sell_or_License_Any_File_for_Bitcoin.md', 'prettyName': 'Sell or License Any File for Bitcoin'},
{'url': 'gist.github.com/pkrasam/e79f93a7f7d90a0877bb', 'name': 'gist.07_Bitcoin-Accelerated_Computing.md', 'prettyName': 'Bitcoin-Accelerated Computing'},
{'url': 'gist.github.com/pkrasam/5e010712056c2bdef9e4', 'name': 'gist.08_Intelligent_Agents_with_Bitcoin.md', 'prettyName': 'Intellignet Agents with Bitcoin'},
{'url': 'gist.github.com/pkrasam/faef101460cae1d6d669', 'name': 'gist.09_A_Bitcoin-Payable_Notary_Public.md', 'prettyName': 'A Bitcoin-Payable Notary Public'},
{'url': 'gist.github.com/pkrasam/9bc7b91048a27884e93d', 'name': 'gist.10_A_Crawler_for_the_Machine-Payable_Web.md', 'prettyName': 'A Crawler for the Machine-Payable-Web'},
{'url': 'gist.github.com/pkrasam/0725515d72bb61c023fb', 'name': 'gist.11_Monetize_the_Command_Line_with_Bitcoin.md', 'prettyName': 'Monetize the Command Line with Bitcoin'},
{'url': 'gist.github.com/pkrasam/d4ab02b91f7d2f6fa83d', 'name': 'gist.12_Translate_English_to_Chinese_for_Bitcoin.md', 'prettyName': 'Translate English to Chinese for Bitcoin'}
]
