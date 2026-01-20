from app.model.transaksi import Transaksi
from app.model.barang import Barang
from app.model.supplier import Supplier
from app import db
from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
import string
import random

def generate_kode_transaksi(tipe):
    """Generate unique transaction code"""
    prefix = 'TRM' if tipe == 'masuk' else 'TRK'  # TRM = Transaksi Masuk, TRK = Transaksi Keluar
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{date_str}{random_str}"

def index():
    """Display all transactions"""
    try:
        tipe_filter = request.args.get('tipe', '')
        search = request.args.get('search', '')
        
        query = db.session.query(Transaksi).order_by(Transaksi.tanggal_transaksi.desc())
        
        if tipe_filter:
            query = query.filter(Transaksi.tipe_transaksi == tipe_filter)
        
        if search:
            query = query.join(Barang).filter(
                (Barang.nama_barang.like(f'%{search}%')) |
                (Transaksi.kode_transaksi.like(f'%{search}%'))
            )
        
        data = query.all()
        
        # Calculate summary
        total_masuk = db.session.query(db.func.sum(Transaksi.total_harga))\
            .filter(Transaksi.tipe_transaksi == 'masuk').scalar() or 0
        total_keluar = db.session.query(db.func.sum(Transaksi.total_harga))\
            .filter(Transaksi.tipe_transaksi == 'keluar').scalar() or 0
        
        return render_template('transaksi_index.html', 
                             data=data,
                             total_masuk=total_masuk,
                             total_keluar=total_keluar)
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return render_template('transaksi_index.html', data=[])

def form_tambah():
    """Display form to add new transaction"""
    try:
        tipe = request.args.get('tipe', 'masuk')
        list_barang = Barang.query.order_by(Barang.nama_barang).all()
        list_supplier = Supplier.query.order_by(Supplier.nama_supplier).all()
        kode_transaksi = generate_kode_transaksi(tipe)
        
        return render_template('transaksi_tambah.html',
                             tipe=tipe,
                             list_barang=list_barang,
                             list_supplier=list_supplier,
                             kode_transaksi=kode_transaksi)
    except Exception as e:
        flash(f'Gagal memuat form: {str(e)}', 'danger')
        return redirect(url_for('transaksi_index'))

def save():
    """Save new transaction and update stock"""
    try:
        kode_transaksi = request.form.get('kode_transaksi', '').strip()
        tipe_transaksi = request.form.get('tipe_transaksi', 'masuk')
        barang_id = request.form.get('barang_id')
        supplier_id = request.form.get('supplier_id') or None
        jumlah = request.form.get('jumlah', 0)
        harga_satuan = request.form.get('harga_satuan', 0)
        keterangan = request.form.get('keterangan', '').strip()
        
        # Validation
        if not kode_transaksi:
            flash('Kode transaksi wajib diisi!', 'warning')
            return redirect(url_for('transaksi_add'))
        
        if not barang_id:
            flash('Barang wajib dipilih!', 'warning')
            return redirect(url_for('transaksi_add'))
        
        # Convert to appropriate types
        try:
            jumlah = int(jumlah)
            harga_satuan = int(harga_satuan)
        except ValueError:
            flash('Jumlah dan harga harus berupa angka!', 'warning')
            return redirect(url_for('transaksi_add'))
        
        if jumlah <= 0:
            flash('Jumlah harus lebih dari 0!', 'warning')
            return redirect(url_for('transaksi_add'))
        
        # Get barang
        barang = Barang.query.get(barang_id)
        if not barang:
            flash('Barang tidak ditemukan!', 'warning')
            return redirect(url_for('transaksi_add'))
        
        # Check stock for keluar transaction
        if tipe_transaksi == 'keluar' and barang.stok < jumlah:
            flash(f'Stok tidak mencukupi! Stok tersedia: {barang.stok}', 'danger')
            return redirect(url_for('transaksi_add'))
        
        # Check if kode_transaksi already exists
        existing = Transaksi.query.filter_by(kode_transaksi=kode_transaksi).first()
        if existing:
            flash('Kode transaksi sudah digunakan!', 'warning')
            return redirect(url_for('transaksi_add'))
        
        # Create transaction
        transaksi = Transaksi(
            kode_transaksi=kode_transaksi,
            tipe_transaksi=tipe_transaksi,
            barang_id=barang_id,
            supplier_id=supplier_id,
            jumlah=jumlah,
            harga_satuan=harga_satuan,
            keterangan=keterangan,
            created_by=session.get('user', 'system')
        )
        transaksi.calculate_total()
        
        # Update stock
        try:
            barang.update_stok(jumlah, tipe_transaksi)
        except ValueError as ve:
            flash(str(ve), 'danger')
            return redirect(url_for('transaksi_add'))
        
        db.session.add(transaksi)
        db.session.commit()
        
        flash(f'Transaksi {tipe_transaksi} berhasil ditambahkan!', 'success')
        return redirect(url_for('transaksi_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menyimpan transaksi: {str(e)}', 'danger')
        return redirect(url_for('transaksi_add'))

def detail(id):
    """Display transaction details"""
    try:
        transaksi = Transaksi.query.get(id)
        if not transaksi:
            flash('Transaksi tidak ditemukan!', 'warning')
            return redirect(url_for('transaksi_index'))
        
        return render_template('transaksi_detail.html', data=transaksi)
    except Exception as e:
        flash(f'Gagal memuat detail: {str(e)}', 'danger')
        return redirect(url_for('transaksi_index'))

def delete(id):
    """Delete transaction and revert stock"""
    try:
        transaksi = Transaksi.query.get(id)
        if not transaksi:
            flash('Transaksi tidak ditemukan!', 'warning')
            return redirect(url_for('transaksi_index'))
        
        # Get barang
        barang = transaksi.barang
        
        # Revert stock
        if transaksi.tipe_transaksi == 'masuk':
            # Revert masuk = reduce stock
            if barang.stok >= transaksi.jumlah:
                barang.stok -= transaksi.jumlah
            else:
                flash('Tidak dapat menghapus transaksi: stok tidak mencukupi untuk revert!', 'danger')
                return redirect(url_for('transaksi_index'))
        else:
            # Revert keluar = add stock
            barang.stok += transaksi.jumlah
        
        kode = transaksi.kode_transaksi
        db.session.delete(transaksi)
        db.session.commit()
        
        flash(f'Transaksi "{kode}" berhasil dihapus dan stok telah dikembalikan!', 'success')
        return redirect(url_for('transaksi_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus transaksi: {str(e)}', 'danger')
        return redirect(url_for('transaksi_index'))

def laporan():
    """Display transaction report with date range filter"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        tipe = request.args.get('tipe', '')
        
        query = db.session.query(Transaksi).order_by(Transaksi.tanggal_transaksi.desc())
        
        if start_date:
            query = query.filter(Transaksi.tanggal_transaksi >= start_date)
        if end_date:
            query = query.filter(Transaksi.tanggal_transaksi <= end_date)
        if tipe:
            query = query.filter(Transaksi.tipe_transaksi == tipe)
        
        data = query.all()
        
        # Calculate totals
        total_nilai = sum(t.total_harga for t in data)
        total_qty = sum(t.jumlah for t in data)
        
        return render_template('transaksi_laporan.html',
                             data=data,
                             total_nilai=total_nilai,
                             total_qty=total_qty,
                             start_date=start_date,
                             end_date=end_date,
                             tipe=tipe)
    except Exception as e:
        flash(f'Gagal memuat laporan: {str(e)}', 'danger')
        return render_template('transaksi_laporan.html', data=[])
