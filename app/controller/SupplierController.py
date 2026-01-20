from app.model.supplier import Supplier
from app import db
from sqlalchemy import text
from flask import render_template, request, redirect, url_for, flash

def index():
    """Display all suppliers"""
    try:
        search = request.args.get('search', '')
        
        query = Supplier.query
        if search:
            query = query.filter(
                (Supplier.nama_supplier.like(f'%{search}%')) | 
                (Supplier.kontak_supplier.like(f'%{search}%'))
            )
        
        data = query.order_by(Supplier.nama_supplier).all()
        return render_template('supplier_index.html', data=data)
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return render_template('supplier_index.html', data=[])

def form_tambah():
    """Display form to add new supplier"""
    return render_template('supplier_tambah.html')

def save():
    """Save new supplier with validation"""
    try:
        nama = request.form.get('nama_supplier', '').strip()
        kontak = request.form.get('kontak_supplier', '').strip()
        email = request.form.get('email', '').strip()
        alamat = request.form.get('alamat', '').strip()
        keterangan = request.form.get('keterangan', '').strip()
        
        # Validation
        if not nama:
            flash('Nama supplier wajib diisi!', 'warning')
            return redirect(url_for('supplier_add'))
        
        if not kontak:
            flash('Kontak supplier wajib diisi!', 'warning')
            return redirect(url_for('supplier_add'))
        
        # Check if supplier already exists
        existing = Supplier.query.filter_by(nama_supplier=nama).first()
        if existing:
            flash('Supplier dengan nama tersebut sudah ada!', 'warning')
            return redirect(url_for('supplier_add'))
        
        supplier_baru = Supplier(
            nama_supplier=nama,
            kontak_supplier=kontak,
            email=email,
            alamat=alamat,
            keterangan=keterangan
        )
        db.session.add(supplier_baru)
        db.session.commit()
        
        flash(f'Supplier "{nama}" berhasil ditambahkan!', 'success')
        return redirect(url_for('supplier_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menyimpan supplier: {str(e)}', 'danger')
        return redirect(url_for('supplier_add'))

def form_edit(id):
    """Display form to edit supplier"""
    try:
        supplier = Supplier.query.get(id)
        if not supplier:
            flash('Supplier tidak ditemukan!', 'warning')
            return redirect(url_for('supplier_index'))
        return render_template('supplier_edit.html', data=supplier)
    except Exception as e:
        flash(f'Gagal memuat form: {str(e)}', 'danger')
        return redirect(url_for('supplier_index'))

def update(id):
    """Update existing supplier with validation"""
    try:
        supplier = Supplier.query.get(id)
        if not supplier:
            flash('Supplier tidak ditemukan!', 'warning')
            return redirect(url_for('supplier_index'))
        
        nama = request.form.get('nama_supplier', '').strip()
        kontak = request.form.get('kontak_supplier', '').strip()
        email = request.form.get('email', '').strip()
        alamat = request.form.get('alamat', '').strip()
        keterangan = request.form.get('keterangan', '').strip()
        
        # Validation
        if not nama:
            flash('Nama supplier wajib diisi!', 'warning')
            return redirect(url_for('supplier_edit', id=id))
        
        if not kontak:
            flash('Kontak supplier wajib diisi!', 'warning')
            return redirect(url_for('supplier_edit', id=id))
        
        # Check if supplier name already exists (excluding current)
        existing = Supplier.query.filter(
            Supplier.nama_supplier == nama,
            Supplier.id != id
        ).first()
        if existing:
            flash('Supplier dengan nama tersebut sudah ada!', 'warning')
            return redirect(url_for('supplier_edit', id=id))
        
        supplier.nama_supplier = nama
        supplier.kontak_supplier = kontak
        supplier.email = email
        supplier.alamat = alamat
        supplier.keterangan = keterangan
        db.session.commit()
        
        flash(f'Supplier "{nama}" berhasil diupdate!', 'success')
        return redirect(url_for('supplier_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal update supplier: {str(e)}', 'danger')
        return redirect(url_for('supplier_edit', id=id))

def delete(id):
    """Delete supplier"""
    try:
        supplier = Supplier.query.get(id)
        if not supplier:
            flash('Supplier tidak ditemukan!', 'warning')
            return redirect(url_for('supplier_index'))
        
        # Check if supplier has items
        if supplier.barang.count() > 0:
            flash('Tidak dapat menghapus supplier yang masih terhubung dengan barang!', 'danger')
            return redirect(url_for('supplier_index'))
        
        nama_supplier = supplier.nama_supplier
        db.session.delete(supplier)
        db.session.commit()
        
        flash(f'Supplier "{nama_supplier}" berhasil dihapus!', 'success')
        return redirect(url_for('supplier_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal hapus supplier: {str(e)}', 'danger')
        return redirect(url_for('supplier_index'))

def detail(id):
    """Display supplier details with associated items"""
    try:
        supplier = Supplier.query.get(id)
        if not supplier:
            flash('Supplier tidak ditemukan!', 'warning')
            return redirect(url_for('supplier_index'))
        
        # Get items from this supplier
        barang_list = supplier.barang.all()
        transaksi_list = supplier.transaksi.order_by(text('tanggal_transaksi desc')).limit(10).all()
        
        return render_template('supplier_detail.html', 
                             supplier=supplier,
                             barang_list=barang_list,
                             transaksi_list=transaksi_list)
    except Exception as e:
        flash(f'Gagal memuat detail: {str(e)}', 'danger')
        return redirect(url_for('supplier_index'))
