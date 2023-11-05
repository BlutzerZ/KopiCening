from app import app, db
from models import Product as ProductModels, ProductColor as ProductColorModels, ProductSize as ProductSizeModels, ProductStock as ProductStockModels, Transaction as OrderModels, TransactionItem as OrderItemModels
from flask import render_template, request, session, redirect, abort, u
rl_for, render_template
import time, os, random
from pytz import timezone
from datetime import datetime
from werkzeug.utils import secure_filename

@app.before_request
def before_request():
    session.setdefault('user', None)
    session.setdefault('hpp', 0)

@app.route("/login", methods=['GET', 'POST'])
def admin_login_form():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        if email == 'ridwaniko09@gmail.com' and pwd == 'SIDEMIT ADMIN':
            session['user'] = 'admin'
            print("login sucess")
            return redirect(url_for('admin_dashboard'))
        
    return render_template('login.html')

@app.route("/logout")
def admin_logout():
    session.pop('user', None)
    return redirect(url_for('show_all_product'))
