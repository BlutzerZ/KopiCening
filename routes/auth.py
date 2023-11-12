from app import app, db
from flask import render_template, request, session, redirect, abort, url_for, render_template
import time, os, random
from pytz import timezone
from datetime import datetime
from werkzeug.utils import secure_filename

@app.before_request
def before_request():
    session.setdefault('userID', None)
    session.setdefault('hpp', 0)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        if email == 'admin' and pwd == 'admin':
            session['userID'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        
    return render_template('dashboard/login.html')

@app.route("/logout")
def admin_logout():
    session.pop('userID', None)
    return redirect(url_for('login'))
