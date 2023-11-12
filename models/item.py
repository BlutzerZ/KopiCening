import time
from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    type = db.Column(db.Integer)
    name = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)
    transactionItem = db.relationship('ItemAddon', backref='item')

class ItemAddon(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)
    tid = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

