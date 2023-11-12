from app import app, db
from models.product import Product as ProductModels
from models.transactions import Transaction as OrderModels, TransactionItem as OrderItemModels
from flask import render_template, request, session, redirect, abort, url_for, render_template
import time, os, random
from pytz import timezone
from datetime import datetime
from werkzeug.utils import secure_filename


# Product routes ===============================

@app.route("/")
def home():
    products = ProductModels.query.all()

    return render_template('ecommerce/index.html', products=products)

# CART ROUTES ========

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    if request.method == "POST":
        cart = session.get('keranjang', [])
        cart.append({
            "id": request.form['fid'],
            "img": request.form['fimg'],
            "title": request.form['ftitle'],
            "jumlah": request.form['fjumlah'],
            "harga": request.form['fharga'],
            "total": int(request.form['fjumlah']) * int(request.form['fharga']),
        })
        session['keranjang'] = cart
        return redirect(url_for('cart'))
    else:
        items = session.get('keranjang', [])
        return render_template('ecommerce/cart.html', items=items)

@app.route("/delete-cart-all/")
def delete_cart_all():
    session.pop('keranjang', None)
    return redirect(url_for('show_all_product'))

@app.route("/delete-cart/<int:item_id>", methods=["POST"])
def delete_cart(item_id):
    for i, item in enumerate(session.get('keranjang', [])):
        if int(item['id']) == item_id:
            print("found")
            cart = session.get('keranjang', [])
            cart.pop(i)
            session['keranjang'] = cart
            break
    return redirect(url_for('cart'))



# Checkout =======================================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        total = int(request.form['ftotal'])
        return render_template('ecommerce/checkout.html', total=total)

    else:
        return "<p>Nothing here</p>"

@app.route("/checkout/success", methods=["POST"])
def checkout_success():
        fname = request.form['fname']
        faddress = request.form['faddress']
        fphone = request.form['fphone']
        ftotal = request.form['ftotal']
        ftotal = request.form['ftotal']
        fpaid = request.form['paid']
        while True:
            randomID = random.randint(0, 99999999)
            dummyCheck = db.session.query(OrderModels).filter(OrderModels.id == randomID).first()
            if dummyCheck is None:
                db_item = OrderModels(
                    id=randomID,
                    name=fname,
                    address=faddress,
                    phone=fphone,
                    total=ftotal,
                    paidStatus=fpaid,
                )
                db.session.add(db_item)
                db.session.commit()
                db.session.refresh(db_item)
                break

        carts = session.get('keranjang', [])
        for cart in carts:
            db_item = OrderItemModels(
                title=cart['title'],
                price=cart['harga'],
                jumlah=cart['jumlah'],
                total=cart['total'],
                tid=randomID
            )

            db.session.add(db_item)

            product = ProductModels.query.filter_by(id=cart['id']).first()
            product.stock = int(product.stock) - int(cart['jumlah'])
            print(f"delete id {cart['id']} mined {cart['jumlah']}")
        
        db.session.commit()
        db.session.refresh(db_item)

        session.pop('keranjang', None)
        return 'success'