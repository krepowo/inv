from flask import request, session, redirect, url_for, render_template, flash
from functools import wraps

from app import app
from app.controller import InventoryController
from app.controller import KategoriController
from app.controller import UserController
from app.controller import SupplierController
from app.controller import TransaksiController
from app.model.barang import Barang
from app.model.transaksi import Transaksi
from app import db

# Decorator untuk check login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Silakan login terlebih dahulu!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator untuk check admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Silakan login terlebih dahulu!', 'warning')
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash('Anda tidak memiliki akses ke halaman ini!', 'danger')
            return redirect(url_for('inventory_index'))
        return f(*args, **kwargs)
    return decorated_function

# Auth Routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    return UserController.login()

@app.route("/logout")
def logout():
    return UserController.logout()

@app.route("/register", methods=['GET', 'POST'])
@admin_required
def register():
    return UserController.register()

@app.route("/users")
@admin_required
def user_list():
    return UserController.user_list()

# Dashboard
@app.route('/')
@login_required
def dashboard():
    try:
        # Get statistics
        total_barang = Barang.query.count()
        total_stok = db.session.query(db.func.sum(Barang.stok)).scalar() or 0
        low_stock_items = Barang.query.filter(Barang.stok <= Barang.stok_minimum).all()
        
        # Recent transactions
        recent_transactions = Transaksi.query.order_by(Transaksi.tanggal_transaksi.desc()).limit(5).all()
        
        # Transaction summary (this month)
        from datetime import datetime, timedelta
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        transaksi_masuk = db.session.query(db.func.sum(Transaksi.total_harga))\
            .filter(Transaksi.tipe_transaksi == 'masuk',
                   Transaksi.tanggal_transaksi >= start_of_month).scalar() or 0
        
        transaksi_keluar = db.session.query(db.func.sum(Transaksi.total_harga))\
            .filter(Transaksi.tipe_transaksi == 'keluar',
                   Transaksi.tanggal_transaksi >= start_of_month).scalar() or 0
        
        return render_template('dashboard.html',
                             total_barang=total_barang,
                             total_stok=total_stok,
                             low_stock_items=low_stock_items,
                             recent_transactions=recent_transactions,
                             transaksi_masuk=transaksi_masuk,
                             transaksi_keluar=transaksi_keluar)
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return render_template('dashboard.html')

# CRUD Inventory/Barang
@app.route('/inventory')
@login_required
def inventory_index():
    return InventoryController.index()

@app.route('/inventory/tambah', methods=['GET', 'POST'])
@login_required
def inventory_add():
    if request.method == 'GET':
        return InventoryController.form_tambah()
    else:
        return InventoryController.save()

@app.route('/inventory/edit/<id>', methods=['GET'])
@login_required
def inventory_edit(id):
    return InventoryController.form_edit(id)

@app.route('/inventory/update/<id>', methods=['POST'])
@login_required
def inventory_update(id):
    return InventoryController.update(id)

@app.route('/inventory/hapus/<id>')
@login_required
def inventory_delete(id):
    return InventoryController.delete(id)

# CRUD Kategori
@app.route('/kategori')
@login_required
def kategori_index():
    return KategoriController.index()

@app.route('/kategori/tambah', methods=['GET', 'POST'])
@login_required
def kategori_add():
    if request.method == 'GET':
        return KategoriController.form_tambah()
    else:
        return KategoriController.save()

@app.route('/kategori/edit/<id>', methods=['GET'])
@login_required
def kategori_edit(id):
    return KategoriController.form_edit(id)

@app.route('/kategori/update/<id>', methods=['POST'])
@login_required
def kategori_update(id):
    return KategoriController.update(id)

@app.route('/kategori/hapus/<id>')
@login_required
def kategori_delete(id):
    return KategoriController.delete(id)

# CRUD Supplier
@app.route('/supplier')
@login_required
def supplier_index():
    return SupplierController.index()

@app.route('/supplier/tambah', methods=['GET', 'POST'])
@login_required
def supplier_add():
    if request.method == 'GET':
        return SupplierController.form_tambah()
    else:
        return SupplierController.save()

@app.route('/supplier/edit/<id>', methods=['GET'])
@login_required
def supplier_edit(id):
    return SupplierController.form_edit(id)

@app.route('/supplier/update/<id>', methods=['POST'])
@login_required
def supplier_update(id):
    return SupplierController.update(id)

@app.route('/supplier/hapus/<id>')
@login_required
def supplier_delete(id):
    return SupplierController.delete(id)

@app.route('/supplier/detail/<id>')
@login_required
def supplier_detail(id):
    return SupplierController.detail(id)

# Transaksi
@app.route('/transaksi')
@login_required
def transaksi_index():
    return TransaksiController.index()

@app.route('/transaksi/tambah', methods=['GET', 'POST'])
@login_required
def transaksi_add():
    if request.method == 'GET':
        return TransaksiController.form_tambah()
    else:
        return TransaksiController.save()

@app.route('/transaksi/detail/<id>')
@login_required
def transaksi_detail(id):
    return TransaksiController.detail(id)

@app.route('/transaksi/hapus/<id>')
@login_required
def transaksi_delete(id):
    return TransaksiController.delete(id)

@app.route('/transaksi/laporan')
@login_required
def transaksi_laporan():
    return TransaksiController.laporan()