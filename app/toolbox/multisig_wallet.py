import os
import requests
import json

DEFAULT_WALLET_PATH = os.path.join(os.path.expanduser('~'),
                                   ".two1",
                                   "wallet",
                                   "multisig_wallet.json")

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

class multisig_wallet(object):

    @staticmethod
    def create_wallet(username, passphrase):
        ## Create a new wallet using BitGo Express 
        payload = json.dumps({ "passphrase": passphrase, "label": username })
        try:
            r = requests.post('http://localhost:3080/api/v1/wallets/simplecreate',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'},
                              data = payload)
        except:
            print('Please ensure that you have BitGo Express running on your local machine')
            return 
        print(r.json())
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
                
    @staticmethod        
    def send_bitcoin(sender, address, amount, passphrase):
        print('Sending Bitcoin')
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
            print('User does not exist')
            return
            
        print('Amount is: ' + amount)
        payload = json.dumps({"address": address, "amount": int(amount), "walletPassphrase": passphrase})
        #use the sender username to look up the sender id
        try:
            r = requests.post('http://localhost:3080/api/v1/wallet/' + walletId + '/sendcoins',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'},
                              data = payload)
        except:
            print('Please ensure that you have BitGo Express running on your local machine')
            return

        print(r.json())

    @staticmethod
    def generate_address(username):
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

        ## Ensure that the user exists
        try:
            walletId
        except NameError:
            print('User does not exist')            
            return

        try:
            r = requests.post('http://localhost:3080/api/v1/wallet/' + walletId + '/address/0',
                              headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'})
        except:
            print('Please ensure that you have BitGo Express running on your local machine')
            return

        print('Generated address for ' + username + ':')       
        print(r.json()['address'])
        return r.json()['address']

    @staticmethod
    def get_balance(username):
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

        ## Ensure that the user exists
        try:
            walletId
        except NameError:
            print('User does not exist')
            return

        try:
            r = requests.get('http://localhost:3080/api/v1/wallet/' + walletId,
                        headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'content-type': 'application/json'})
        except:
            print('Please ensure that you have BitGo Express running on your local machine')
            return

        print('Balance for ' + username + ' is: ')
        print(r.json()['balance'])

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
            print('Please ensure that you have BitGo Express running on your local machine')
            return
            
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
            print('Please ensure that you have BitGo Express running on your local machine')
            return
            
        print(r.json())

    @staticmethod        
    def ping():
        r = requests.post('http://localhost:3080/api/v1/ping', headers = {'Authorization': 'Bearer ' + access_token})
        print(r.json())

