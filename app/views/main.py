from functools import wraps
from flask import render_template, jsonify, session, redirect
from app import app
import random

def login_required(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        print 'test'
        if 'email' in session:
            print session['email']
        else:
            return redirect('/')
        return func(*args, **kwargs)
    return func_wrapper

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
@login_required
def map():
    return render_template('map.html', title='Map')

@app.route('/wallet')
@login_required
def wallet():
    return render_template('wallet.html', title='Wallet')

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
