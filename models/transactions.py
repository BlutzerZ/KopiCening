import time
from app import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    total = db.Column(db.Integer)
    paidStatus = db.Column(db.String(3))
    createdAt = db.Column(db.Integer, default=time.time()) # unix time format
    transactionItem = db.relationship('TransactionItem', backref='transaction')

class TransactionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Integer)
    jumlah = db.Column(db.Integer)
    total = db.Column(db.Integer, default=price*jumlah)
    tid = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)