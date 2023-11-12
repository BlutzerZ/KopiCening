from app import app, db
from models.product import Product as ProductModels
from models.transactions import Transaction as OrderModels
from models.transactions import TransactionItem as OrderItemModels
from models.akun import Akun as AkunModels
from models.akun import AkunTransaction as AkunTransactionModels
from models.product import Product as ProductModels
from flask import render_template, request, session, redirect, abort, url_for, render_template
import time, os, random
from pytz import timezone
from datetime import datetime
from werkzeug.utils import secure_filename

@app.route("/dashboard")
def admin_dashboard():
    if session["userID"] == None:
        return redirect(url_for("login"))
    # KAS
    saldoAwal = {}
    saldoAwal['date'] = ""
    saldoAwal['ref'] = ""
    saldoAwal['keterangan'] = "Saldo Awal"
    saldoAwal['amount'] = 20000000

    totalKas = saldoAwal['amount']

    transactions = AkunTransactionModels.query.all()
    kasFlows = []
    for t in transactions:
        kasFlow = {}
        # date
        kasFlow['date'] = t.createdAt
        # ref
        if t.akunID[0] == "1":
            kasFlow['ref'] = "kas"
        elif t.akunID[0] == "2":
            kasFlow['ref'] = "biaya"
        elif t.akunID[0] == "3":
            kasFlow['ref'] = "pembelian"
        elif t.akunID[0] == "4":
            kasFlow['ref'] = "penjualan"
        else:
            continue
        # keterangan
        if t.akunID[0] == "1" or t.akunID[0] == "2" or t.akunID[0] == "4":
            kasFlow['keterangan'] = t.keterangan
        else:
            kasFlow['keterangan'] = '-'
        # jumlah
        if t.akunID[0] == "4" or t.akunID[0] == "1":
            kasFlow['amount'] = t.amount
        else:
            kasFlow['amount'] = -(t.amount)
        
        kasFlows.append(kasFlow)
        totalKas+= kasFlow['amount']

    # piutang
    saldoAwal = {}
    saldoAwal['date'] = ""
    saldoAwal['ref'] = ""
    saldoAwal['keterangan'] = "Saldo Awal"
    saldoAwal['amount'] = 1000000

    totalPiutang = saldoAwal['amount']

    akunTransactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID == 111).all()
    for t in akunTransactions:
        totalPiutang+=t.amount
    
    orderTransactions = db.session.query(OrderModels).filter(OrderModels.paidStatus == "no").all()
    for t in orderTransactions:
        totalPiutang+=t.total

    # persediaan Barang 
    totPersediaan = 0
    products = ProductModels.query.all()
    for p in products:
        totPersediaan+=p.stock*p.priceBase

    # perlengkapan
    totalPerlengkapan = 0
    transactions = AkunTransactionModels.query.filter_by(akunID = 311).all()
    for t in transactions:
        totalPerlengkapan += int(t.amount)

    # peralatan
    totalPeralatan = 0
    transactions = AkunTransactionModels.query.filter_by(akunID = 312).all()
    for t in transactions:
        totalPeralatan += int(t.amount)

    # aset
    totalAset = 0
    transactions = AkunTransactionModels.query.filter_by(akunID = 313).all()
    for t in transactions:
        totalAset += int(t.amount)

    # modal
    modalAwal = 0
    transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('114')).all()
    for t in transactions:
        modalAwal += t.amount

    # hutang
    totHutang = 0
    hutangSuplier = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID == 112, AkunTransactionModels.amount > 0).all()
    totHutangSuplier = 0
    for hs in hutangSuplier:
        totHutangSuplier+= hs.amount
    
    hutangBisnis = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('3%'), AkunTransactionModels.paid == "no").all()
    totHutangBisnis = 0
    for hb in hutangBisnis:
        totHutangBisnis+= hb.amount
    totHutang = totHutangSuplier + totHutangBisnis

    # profit
    totProfit = 0
    penjualan = 0
    transactions = OrderItemModels.query.all()
    for t in transactions:
        penjualan += t.total


    totPersediaan = 0
    products = ProductModels.query.all()
    for p in products:
        totPersediaan+=p.stock*p.priceBase

    totPembelian = 0
    transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('3%')).all()
    for t in transactions:
        totPembelian += t.amount

    totBiaya = 0
    transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('2%')).all()
    for t in transactions:
        totBiaya += t.amount

    modalAwal = 0
    transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('114')).all()
    for t in transactions:
        modalAwal += t.amount
    totProfit = int(penjualan) - int(totPersediaan) - int(totPembelian) + int(totPersediaan) + totBiaya
    

    details = {
        "kas": totalKas,
        "piutang": totalPiutang,
        "persediaanBarang": totPersediaan,
        "perlengkapan": totalPerlengkapan,
        "peralatan":totalPeralatan,
        "asetLain": totalAset,
        "jumlahAktiva": totalKas + totalPiutang + totPersediaan + totalPerlengkapan + totalPeralatan + totalAset,

        "modal": modalAwal,
        "hutang": totHutang,
        "profit": totProfit,
        "jumlahPasiva": modalAwal+totHutang+totProfit,
    }

    return  render_template('dashboard/dashboard.html', details=details)

@app.route("/dashboard/input-kas", methods=["GET" ,"POST"])
def dashboard_input_kas():
    if session["userID"] == None:
        return redirect(url_for("login"))
    if request.method == "GET":
        akuns = db.session.query(AkunModels).filter(AkunModels.id.like('1%')).all()
        transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('1%')).all()

        details = {
            'pageName': 'Kas',
            'akuns': akuns,
            'transactions': transactions,
        }
        return  render_template('dashboard/input/inputKasxBiaya.html', details=details)
    
    else:
        date = request.form['date']
        akunID = request.form['akunid']
        keterangan = request.form['keterangan']
        amount = request.form['amount']

        dbItem = AkunTransactionModels(
            createdAt = date,
            akunID = akunID,
            akunName = AkunModels.query.filter_by(id=akunID).first().name,
            keterangan = keterangan,
            amount = amount,
        )

        db.session.add(dbItem)
        db.session.commit()
        db.session.refresh(dbItem)

        return redirect(url_for('dashboard_input_kas'))


@app.route("/dashboard/input-biaya", methods=["GET" ,"POST"])
def dashboard_input_biaya():
    if session["userID"] == None:
        return redirect(url_for("login"))
    if request.method == "GET":
        akuns = db.session.query(AkunModels).filter(AkunModels.id.like('2%')).all()
        transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('2%')).all()

        details = {
            'pageName': 'Biaya',
            'akuns': akuns,
            'transactions': transactions,
        }
        return  render_template('dashboard/input/inputKasxBiaya.html', details=details)
    else:
        date = request.form['date']
        akunID = request.form['akunid']
        amount = request.form['amount']

        dbItem = AkunTransactionModels(
            createdAt = date,
            akunID = akunID,
            akunName = AkunModels.query.filter_by(id=akunID).first().name,
            amount = amount,
        )

        db.session.add(dbItem)
        db.session.commit()
        db.session.refresh(dbItem)

        return redirect(url_for('dashboard_input_biaya'))

@app.route("/dashboard/input-pembelian", methods=["GET" ,"POST"])
def dashboard_input_pembelian():
    if session["userID"] == None:
        return redirect(url_for("login"))
    if request.method == "GET":
        akuns = db.session.query(AkunModels).filter(AkunModels.id.like('3%')).all()
        transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('3%')).all()


        details = {
            'pageName': 'Pembelian',
            'akuns': akuns,
            'transactions': transactions,
        }
        return  render_template('dashboard/input/inputPembelian.html', details=details)
    else:
        date = request.form['date']
        akunID = request.form['akunid']
        keterangan = request.form['keterangan']
        qty = request.form['qty']
        price = request.form['price']

        dbItem = AkunTransactionModels(
            createdAt = date,
            akunID = akunID,
            akunName = AkunModels.query.filter_by(id=akunID).first().name,
            keterangan = keterangan,
            qty = qty,
            price = price,
            amount = int(qty)*int(price),
        )

        db.session.add(dbItem)
        db.session.commit()
        db.session.refresh(dbItem)

        return redirect(url_for('dashboard_input_pembelian'))

# DELETE METHOD
@app.route("/dashboard/input-kas/delete", methods=["POST"])
def dashboard_input_kas_delete():
    if session["userID"] == None:
        return redirect(url_for("login"))
    if request.method == "POST":
        tid = request.form['id']
        AkunTransactionModels.query.filter_by(id = tid).delete()
        db.session.commit()
        return redirect(url_for('dashboard_input_kas'))

@app.route("/dashboard/input-biaya/delete", methods=["POST"])
def dashboard_input_biaya_delete():
    if session["userID"] == None:
        return redirect(url_for("login"))
    if request.method == "POST":
        tid = request.form['id']
        AkunTransactionModels.query.filter_by(id = tid).delete()
        db.session.commit()
        return redirect(url_for('dashboard_input_biaya'))
    
@app.route("/dashboard/input-pembelian/delete", methods=["POST"])
def dashboard_input_pembelian_delete():
    if session["userID"] == None:
        return redirect(url_for("login"))
    if request.method == "POST":
        tid = request.form['id']
        AkunTransactionModels.query.filter_by(id = tid).delete()
        db.session.commit()
        return redirect(url_for('dashboard_input_pembelian'))


@app.route("/dashboard/kas")
def dashboard_kas():
    if session["userID"] == None:
        return redirect(url_for("login"))
    saldoAwal = {}
    saldoAwal['date'] = ""
    saldoAwal['ref'] = ""
    saldoAwal['keterangan'] = "Saldo Awal"
    saldoAwal['amount'] = 20000000

    total = saldoAwal['amount']

    transactions = AkunTransactionModels.query.all()
    kasFlows = []
    for t in transactions:
        kasFlow = {}
        # date
        kasFlow['date'] = t.createdAt
        # ref
        if t.akunID[0] == "1":
            kasFlow['ref'] = "kas"
        elif t.akunID[0] == "2":
            kasFlow['ref'] = "biaya"
        elif t.akunID[0] == "3":
            kasFlow['ref'] = "pembelian"
        elif t.akunID[0] == "4":
            kasFlow['ref'] = "penjualan"
        else:
            continue
        # keterangan
        if t.akunID[0] == "1" or t.akunID[0] == "4":
            kasFlow['keterangan'] = t.keterangan
        else:
            kasFlow['keterangan'] = '-'
        # jumlah
        if t.akunID[0] == "4" or t.akunID[0] == "1":
            kasFlow['amount'] = t.amount
        else:
            kasFlow['amount'] = -(t.amount)
        
        kasFlows.append(kasFlow)
        total+= kasFlow['amount']


    return  render_template('dashboard/kas.html', judul="Laporan Arus Kas", saldoAwal=saldoAwal, kasFlow=kasFlows, total=total) 


@app.route("/dashboard/piutang")
def dashboard_piutang():
    if session["userID"] == None:
        return redirect(url_for("login"))
    saldoAwal = {}
    saldoAwal['date'] = ""
    saldoAwal['ref'] = ""
    saldoAwal['keterangan'] = "Saldo Awal"
    saldoAwal['amount'] = 1000000

    total = saldoAwal['amount']

    transactions = []
    akunTransactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID == 111).all()
    for t in akunTransactions:
        transaction = {}
        transaction['date'] = t.createdAt.strftime('%d %b %Y')
        transaction['ref'] = "Kas"
        transaction['keterangan'] = t.keterangan
        transaction['amount'] = t.amount
        transactions.append(transaction)
        total+=t.amount
    
    orderTransactions = db.session.query(OrderModels).filter(OrderModels.paidStatus == "no").all()
    for t in orderTransactions:
        transaction = {}

        utc_time = datetime.utcfromtimestamp(t.createdAt)
        jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
        transaction['date'] = jakarta_time.strftime('%d %b %Y')
        transaction['ref'] = "Penjualan"
        transaction['keterangan'] = t.name
        transaction['amount'] = t.total
        transactions.append(transaction)
        total+=t.total

    return  render_template('dashboard/kas.html', judul="Piutang", saldoAwal=saldoAwal, kasFlow=transactions, total=total) 

@app.route("/dashboard/inventory", methods=["GET", "POST"])
def dashboard_inventory():
    if session["userID"] == None:
        return redirect(url_for("login"))
    
    if request.method == "GET":
        products = ProductModels.query.all()
        tot = 0
        for p in products:
            tot+=p.stock*p.priceBase

        return  render_template('dashboard/inventory.html', products=products, tot=tot) 
    
    else:
        id = request.form['id']
        stock = request.form['qty']
        priceBase = request.form['hrgawal']
        price = request.form['hrgakhir']


        product = db.session.query(ProductModels).get(id)
        product.stock = stock
        product.priceBase = priceBase
        product.price = price
        db.session.commit()

        return redirect(url_for('dashboard_inventory'))

@app.route("/dashboard/perlengkapan")
def dashboard_perlengkapan():
    if session["userID"] == None:
        return redirect(url_for("login"))
    
    judul = "Perlengkapan"

    transactions = AkunTransactionModels.query.filter_by(akunID = 311).all()
    total = 0
    for t in transactions:
        total += int(t.amount)

    return  render_template('dashboard/perlengkapanxPeralatanxAset.html', judul=judul, transactions=transactions, total=total) 

@app.route("/dashboard/peralatan")
def dashboard_peralatan():
    if session["userID"] == None:
        return redirect(url_for("login"))
    
    judul = "Peralatan"

    transactions = AkunTransactionModels.query.filter_by(akunID = 312).all()
    total = 0
    for t in transactions:
        total += int(t.amount)

    return  render_template('dashboard/perlengkapanxPeralatanxAset.html', judul=judul, transactions=transactions, total=total) 

@app.route("/dashboard/aset")
def dashboard_aset():
    if session["userID"] == None:
        return redirect(url_for("login"))

    judul = "Aset"

    transactions = AkunTransactionModels.query.filter_by(akunID = 313).all()
    total = 0
    for t in transactions:
        total += int(t.amount)
    return  render_template('dashboard/perlengkapanxPeralatanxAset.html', judul=judul, transactions=transactions, total=total) 

@app.route("/dashboard/hutang")
def dashboard_hutang():
    if session["userID"] == None:
        return redirect(url_for("login"))
    
    hutangSuplier = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID == 112, AkunTransactionModels.amount > 0).all()
    totHutangSuplier = 0
    for hs in hutangSuplier:
        totHutangSuplier+= hs.amount
    
    hutangBisnis = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('3%'), AkunTransactionModels.paid == "no").all()
    totHutangBisnis = 0
    for hb in hutangBisnis:
        totHutangBisnis+= hb.amount


    details = {
        "totHutangSuplier": totHutangSuplier,
        "hutangSuplier": hutangSuplier,

        "totHutangBisnis": totHutangBisnis,
        "hutangBisnis": hutangBisnis,
    }

    return render_template('dashboard/hutang.html', details=details) 

@app.route("/dashboard/profit")
def dashboard_profit():
    if session["userID"] == None:
        return redirect(url_for("login"))

    penjualan = 0
    transactions = OrderItemModels.query.all()
    for t in transactions:
        penjualan += t.total


    # hpp
    totPersediaan = 0
    products = ProductModels.query.all()
    for p in products:
        totPersediaan+=p.stock*p.priceBase

    totPembelian = 0
    transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('3%')).all()
    for t in transactions:
        totPembelian += t.amount

    totBiaya = 0
    transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('2%')).all()
    for t in transactions:
        totBiaya += t.amount

    # Perubahan Modal
    modalAwal = 0
    transactions = db.session.query(AkunTransactionModels).filter(AkunTransactionModels.akunID.like('114')).all()
    for t in transactions:
        modalAwal += t.amount

    details = {
        "penjualan": penjualan,
        "returPenjualan": 0,
        "potonganPenjualan": 0,
        "penjualanBersih": penjualan,

        "persediaanBarangDagang": totPersediaan,
        "pembelian": totPembelian,
        "returPembelian": 0,
        "potonganPembelian": 0,
        "hargaPokokPembelian": totPembelian,
        "barangPersediaanUntukDijual": int(totPersediaan) - int(totPembelian),
        "persediaanBarangDagangAkhir": totPersediaan,
        "hargaPokokPenjualan": int(totPersediaan) - int(totPembelian) + int(totPersediaan),
        "LabaRugiKotorPenjualan": int(penjualan) - int(totPersediaan) - int(totPembelian) + int(totPersediaan),

        "biayaUsaha": totBiaya,

        "labaRugiSebelumPajak": int(penjualan) - int(totPersediaan) - int(totPembelian) + int(totPersediaan) + totBiaya,
    

        "modalAwal": modalAwal,
        "total": int(modalAwal) + (int(penjualan) - int(totPersediaan) - int(totPembelian) + int(totPersediaan) + totBiaya) ,
    }

    return  render_template('dashboard/profit.html', details=details) 


@app.route("/dashboard/transaction")
def dashboard_transaction():
    if session["userID"] == None:
        return redirect(url_for("login"))
    
    transactions = db.session.query(OrderModels).join(OrderItemModels).group_by(OrderModels.id).order_by(db.func.count().desc()).all()
    # convert time
    for transaction in transactions:
        utc_time = datetime.utcfromtimestamp(transaction.createdAt)
        jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
        transaction.createdAt = jakarta_time.strftime('%d %b %Y')
    return render_template("dashboard/transactions.html", transactions=transactions)    
