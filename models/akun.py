import time
from app import db
import datetime
import pytz

class Akun(db.Model):
    id = db.Column(db.String(7), primary_key=True, unique=True)
    name = db.Column(db.String(200), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")   )

class AkunTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    akunName = db.Column(db.String(100))
    keterangan = db.Column(db.String(100))
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    paid = db.Column(db.String(10), default="yes")
    createdAt = db.Column(db.DateTime, default=datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d"))
    akunID = db.Column(db.String(7), db.ForeignKey('akun.id'))
    akun = db.relationship('Akun', backref='akun_transactions', lazy=True)
