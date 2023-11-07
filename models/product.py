import time
from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    image = db.Column(db.String(200))
    title = db.Column(db.String(100))
    desc = db.Column(db.String(300))
    price = db.Column(db.String(100))

    