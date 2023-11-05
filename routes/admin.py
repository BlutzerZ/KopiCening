from app import app, db
from models import Product as ProductModels, ProductColor as ProductColorModels, ProductSize as ProductSizeModels, ProductStock as ProductStockModels, Transaction as OrderModels, TransactionItem as OrderItemModels
from flask import render_template, request, session, redirect, abort, url_for, render_template
import time, os, random
from pytz import timezone
from datetime import datetime
from werkzeug.utils import secure_filename

@app.route("/dashboard")
def admin_dashboard():
    if session['user'] != 'admin':
        return redirect(url_for('admin_login_form'))
    return  render_template('dashboard.html')

@app.route("/dashboard/product")
def dashboard_product():
    if session['user'] != 'admin':
        return redirect(url_for('admin_login_form'))
    products = ProductModels.query.all()
    return  render_template('dashboardproduct.html', products=products)

@app.route("/dashboard/hpp")
def dashboard_hpp():
    if session['user'] != 'admin':
        return redirect(url_for('admin_login_form'))
    return  render_template('dashboardhpp.html', hpp=session['hpp']) 

@app.route("/dashboard/transaction")
def dashboard_transaction():
    transactions = db.session.query(OrderModels).join(OrderItemModels).group_by(OrderModels.id).order_by(db.func.count().desc()).all()
    # convert time
    for transaction in transactions:
        utc_time = datetime.utcfromtimestamp(transaction.createdAt)
        jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
        transaction.createdAt = jakarta_time.strftime('%d %b %Y')
    return render_template("dashboardtransaction.html", transactions=transactions)
