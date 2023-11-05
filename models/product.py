import time
from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    image = db.Column(db.String(200))

    title = db.Column(db.String(100))
    desc = db.Column(db.String(300))
    sizes = db.relationship('ProductSize', backref='transaction')


class ProductSize(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    productSize = db.Column(db.String(10))
    productSizePrice = db.Column(db.String(100))
    productID = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    