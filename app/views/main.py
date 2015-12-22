from functools import wraps
from flask import render_template, jsonify, session, redirect, request, json
from app import app
import random
from app.toolbox.multisig_wallet import multisig_wallet

def login_required(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if 'email' in session:
            print session['email']
        else:
            return redirect('/user/signin')
        return func(*args, **kwargs)
    return func_wrapper

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
@login_required
def map():
    return render_template('map.html', title='Map')

@app.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    if request.method == 'GET':
        username = session['email']    
        address = multisig_wallet.generate_address(str(username))    
        balance = multisig_wallet.get_balance(str(username))
        return render_template('wallet.html', title='Wallet', address=address, balance=balance)

    if request.method == 'POST':
        username = session['email']    
        address = multisig_wallet.generate_address(str(username))    
        balance = multisig_wallet.get_balance(str(username))
        return render_template('wallet.html', title='Wallet', address=address, balance=balance)

@app.route('/wallet/generateAddress', methods=['GET'])
@login_required
def wallet_generateAddress():
    username = session['email']    
    address = multisig_wallet.generate_address(str(username))
    return jsonify({'address': address})

@app.route('/map/refresh', methods=['POST'])
@login_required
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html', title='Contact')
