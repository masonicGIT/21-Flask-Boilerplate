from app import app, models
import os, requests, json

DEFAULT_WALLET_PATH = os.path.join(os.path.expanduser('~'),
                                   ".two1",
                                   "wallet",
                                   "multisig_wallet.json")

ACCESS_TOKEN = app.config['ACCESS_TOKEN']

class multisig_wallet(object):

    @staticmethod
    def session():
        print ('calling session')
        try:
            r = requests.get('http://localhost:3080/api/v1/user/session',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'Content-Type': 'application/json'},
                              data = {})
        except:
            print('BitGo Express: ' + 'Please ensure that BitGo Express is running in prod with a')
            print('BitGo Express: ' + 'valid access token from www.bitgo.com')
            return False

        if (r.status_code == 200):
            print(r.status_code)
            return True

        #Unauthorized, dev token is not set or invalid or environment is set to test
        if (r.status_code == 401):
            print(r.status_code)
            print('BitGo Express: ' + r.json()['error'])
            print('BitGo Express: ' + 'Please ensure that BitGo Express is running in prod with a')
            print('BitGo Express: ' + 'valid access token from www.bitgo.com')
            return False

        # Error should be handled prior to this
        return False

    @staticmethod
    def create_wallet(username, passphrase):
        print(passphrase)
        ## Create a new wallet using BitGo Express 
        payload = json.dumps({ "passphrase": passphrase, "label": username })
        try:
            r = requests.post('http://localhost:3080/api/v1/wallets/simplecreate',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'},
                              data = payload)
        
        except:
            print('There was an error retrieving your wallet')

        #Unauthorized, dev token is not set or invalid or environment is set to test
        if (r.status_code == 401):
            print(r.status_code)
            print('BitGo Express: ' + r.json()['error'])
            print('BitGo Express: ' + 'Please ensure that BitGo Express is running in prod with a')
            print('BitGo Express: ' + 'valid access token from www.bitgo.com')
            return False

        ## Setup wallet parameters
        walletId = r.json()['wallet']['id']
        user = r.json()['wallet']['label']
        keychain = r.json()['wallet']['private']        
        newWallet = {user: { "walletId": walletId, "keychain": keychain }}

        ## Save new wallet to bitgo_wallet.json
        try: 
            with open(DEFAULT_WALLET_PATH, 'r') as read_file:
                data = json.load(read_file)
                data.append(newWallet)
        except:
            data = [newWallet]
            
        with open(DEFAULT_WALLET_PATH, 'w') as write_file:
            json.dump(data, write_file)
            print('New user created with: ')
            print('Username: ' + str(user))
            print('Wallet ID: ' + walletId + '\n')
            print('Your wallet config file can be found at: ' + DEFAULT_WALLET_PATH)

        print('Created a new wallet for: ' + username)       
        print(r.json()['wallet']['id'])
        return r.json()['wallet']['id']
        
    @staticmethod
    def generate_address(username):
        try:
            # use username to look up wallet Id
            with open(DEFAULT_WALLET_PATH, 'r') as wallet:
                data = json.loads(wallet.read())
            for user in data:
                try:
                    if user[username]:
                        print('Wallet found')
                        walletId = user[username]['walletId']
                except:
                    print('Loading wallet..')        

        except:
            print('Wallet not found, creating new user...')

        ## Ensure that the user exists
        try:
            walletId
        except NameError:

            print('BitGo Express: User does not exist')            
            print('BitGo Express: Checking API availability..')
            serviceOk = multisig_wallet.session()
            user = models.User.query.filter_by(email=username).first()
            # Create new wallet for user using BitGo
            if (serviceOk == True):
                walletId = multisig_wallet.create_wallet(username, str(user.password))
            # Return if service is down
            if (serviceOk == False):
                return None

        try:
            r = requests.post('http://localhost:3080/api/v1/wallet/' + walletId + '/address/0',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'})

        except:
            print('There was an error with the request')

        if (r.status_code != 200):
            print('BitGo Express: User does not exist')            
            print('BitGo Express: Checking API availability..')
            serviceOk = multisig_wallet.session()
            user = models.User.query.filter_by(email=username).first()
            # Create new wallet for user using BitGo
            if (serviceOk == True):
                walletId = multisig_wallet.create_wallet(username, str(user.password))
            # Return if service is down
            if (serviceOk == False):
                return None

        print('Generated address for ' + username + ':')       
        print(r.json()['address'])
        return r.json()['address']

    @staticmethod
    def get_balance(username):
        try:
            # use username to look up wallet Id
            with open(DEFAULT_WALLET_PATH, 'r') as wallet:
                data = json.loads(wallet.read())
            for user in data:
                try:
                    if user[username]:
                        print('Wallet found')
                        walletId = user[username]['walletId']
                except:
                    print('Loading wallet..')        

        except:
            print('Wallet not found, creating new user...')

        ## Ensure that the user exists
        try:
            walletId
        except NameError:

            print('BitGo Express: User does not exist')            
            print('BitGo Express: Checking API availability..')
            serviceOk = multisig_wallet.session()
            user = models.User.query.filter_by(email=username).first()
            # Create new wallet for user using BitGo
            if (serviceOk == True):
                multisig_wallet.create_wallet(username, str(user.password))
            # Return if service is down
            if (serviceOk == False):
                return None

        try:
            r = requests.get('http://localhost:3080/api/v1/wallet/' + walletId,
                        headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'})

        except:
            print('There was an error retrieving your wallet')

        if (r.status_code == 401):
            print('BitGo Express: User does not exist')            
            print('BitGo Express: Checking API availability..')
            serviceOk = multisig_wallet.session()
            user = models.User.query.filter_by(email=username).first()
            # Create new wallet for user using BitGo
            if (serviceOk == True):
                walletId = multisig_wallet.create_wallet(username, str(user.password))
            # Return if service is down
            if (serviceOk == False):
                return None

        print('Balance for ' + username + ' is: ')
        print(r.json()['balance'])
        return(r.json()['balance'])

    @staticmethod        
    def send_bitcoin(sender, address, amount, passphrase):
        print('Sending Bitcoin')
        if (type(amount) != int):
            return False
        with open(DEFAULT_WALLET_PATH, 'r') as wallet:
          data = json.loads(wallet.read())
        for user in data:
          try:
            if user[sender]:
              print('Wallet found')
              walletId = user[sender]['walletId']
          except:
            print('Loading wallet..')

        ## Ensure that the user exists
        try:
            walletId
        except NameError:

            print('BitGo Express: User does not exist')            
            print('BitGo Express: Checking API availability..')
            serviceOk = multisig_wallet.session()
            user = models.User.query.filter_by(email=username).first()
            # Create new wallet for user using BitGo
            if (serviceOk == True):
                multisig_wallet.create_wallet(username, str(user.password))
            # Return if service is down
            if (serviceOk == False):
                return None
            
        payload = json.dumps({"address": address, "amount": int(amount), "walletPassphrase": passphrase})
        #use the sender username to look up the sender id
        try:
            r = requests.post('http://localhost:3080/api/v1/wallet/' + walletId + '/sendcoins',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'},
                              data = payload)
        except:
            print('Please ensure that you have BitGo Express running on your local machine')

        if (r.status_code == 401):
            print('BitGo Express: User does not exist')            
            print('BitGo Express: Checking API availability..')
            serviceOk = multisig_wallet.session()
            user = models.User.query.filter_by(email=username).first()
            # Create new wallet for user using BitGo
            if (serviceOk == True):
                walletId = multisig_wallet.create_wallet(username, str(user.password))
            # Return if service is down
            if (serviceOk == False):
                return None
        # Insufficient funds, potentially low amount with high fees
        if (r.status_code == 500):
            return r.json()
        # Below the dust threshold
        if (r.status_code == 400):
            return r.json()

        return str(r.json()['hash'])

    @staticmethod
    def set_webhook(username, url, confirms):
        # use username to look up wallet Id
        with open(DEFAULT_WALLET_PATH, 'r') as wallet:
          data = json.loads(wallet.read())
        for user in data:
          try:
            if user[username]:
              print('Wallet found')
              walletId = user[username]['walletId']
          except:
            print('Loading user..')        

        ## Ensure that the user exists
        try:
            walletId
        except NameError:
            print('User does not exist')
            return

        payload = json.dumps({"url": url, "type": "transaction", "numConfirmations": confirms})

        try:
            r = requests.post('http://localhost:3080/api/v1/wallet/' + walletId + '/webhooks',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'},
                              data = payload)
        except:
            print('There was an error retrieving your wallet')

        if (r.status_code == 401):
            return('Error')
            
        print(r.json())

    @staticmethod
    def list_webhooks(username):
        # use username to look up wallet Id
        with open(DEFAULT_WALLET_PATH, 'r') as wallet:
          data = json.loads(wallet.read())
        for user in data:
            try:
                if user[username]:
                    print('Wallet found')
                    walletId = user[username]['walletId']
            except:
                print('Loading user..')        

        ## Ensure that the user exists
        try:
            walletId
        except NameError:
            print('User does not exist')
            return

        try:
            r = requests.get('http://localhost:3080/api/v1/wallet/' + walletId + '/webhooks',
                             headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'})
        except:
            print('There was an error retrieving your wallet')

        if (r.status_code == 401):
            return('Error')
            
        print(r.json())

    @staticmethod        
    def ping():
        r = requests.post('http://localhost:3080/api/v1/ping', headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN})
        print(r.json())


