from app.model.barang import Barang
from app.model.kategori import Kategori
from app.model.supplier import Supplier
from app import db
from flask import render_template, request, redirect, url_for, flash, session
import string
import random

def generate_kode_barang():
    """Buat kode barang yang unik"""
    prefix = 'BRG'
    random_str = ''.join(random.choices(string.digits, k=8))
    return f"{prefix}{random_str}"

def index():
    """Tampilkan semua barang inventory"""
    try:
        search = request.args.get('search', '')
        kategori_filter = request.args.get('kategori', '')
        
        query = db.session.query(Barang)
        
        if search:
            query = query.filter(
                (Barang.nama_barang.like(f'%{search}%')) | 
                (Barang.kode_barang.like(f'%{search}%'))
            )
        
        if kategori_filter:
            query = query.filter(Barang.kategori_id == kategori_filter)
        
        list_barang = query.all()
        list_kategori = Kategori.query.all()
        
        # Hitung jumlah barang stok rendah
        low_stock_count = sum(1 for b in list_barang if b.is_low_stock())
        
        return render_template('barang/index.html', 
                             data=list_barang, 
                             kategori=list_kategori,
                             low_stock_count=low_stock_count)
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return render_template('barang/index.html', data=[], kategori=[], low_stock_count=0)

def form_tambah():
    """Tampilkan form untuk tambah barang baru"""
    try:
        list_kategori = Kategori.query.all()
        list_supplier = Supplier.query.all()
        kode_barang = generate_kode_barang()
        return render_template('barang/tambah.html', 
                             kategori=list_kategori,
                             supplier=list_supplier,
                             kode_barang=kode_barang)
    except Exception as e:
        flash(f'Gagal memuat form: {str(e)}', 'danger')
        return redirect(url_for('inventory_index'))

def save():
    """Simpan barang inventory baru dengan validasi"""
    try:
        # Validasi input
        nama = request.form.get('nama_barang', '').strip()
        kode_barang = request.form.get('kode_barang', '').strip()
        harga_beli = request.form.get('harga_beli', 0)
        harga_jual = request.form.get('harga_jual', 0)
        stok = request.form.get('stok', 0)
        stok_minimum = request.form.get('stok_minimum', 10)
        satuan = request.form.get('satuan', 'pcs')
        kategori_id = request.form.get('kategori_id')
        supplier_id = request.form.get('supplier_id') or None
        deskripsi = request.form.get('deskripsi', '')
        
        # Validasi field yang wajib
        if not nama:
            flash('Nama barang wajib diisi!', 'warning')
            return redirect(url_for('inventory_add'))
        
        if not kode_barang:
            flash('Kode barang wajib diisi!', 'warning')
            return redirect(url_for('inventory_add'))
        
        if not kategori_id:
            flash('Kategori wajib dipilih!', 'warning')
            return redirect(url_for('inventory_add'))
        
        # Cek apakah kode_barang sudah ada
        existing = Barang.query.filter_by(kode_barang=kode_barang).first()
        if existing:
            flash('Kode barang sudah digunakan!', 'warning')
            return redirect(url_for('inventory_add'))
        
        # Konversi ke tipe data yang sesuai
        try:
            harga_beli = int(harga_beli)
            harga_jual = int(harga_jual)
            stok = int(stok)
            stok_minimum = int(stok_minimum)
        except ValueError:
            flash('Harga dan stok harus berupa angka!', 'warning')
            return redirect(url_for('inventory_add'))
        
        # Buat barang baru
        input_barang = Barang(
            kode_barang=kode_barang,
            nama_barang=nama, 
            deskripsi=deskripsi,
            harga_beli=harga_beli,
            harga_jual=harga_jual, 
            stok=stok,
            stok_minimum=stok_minimum,
            satuan=satuan,
            kategori_id=kategori_id,
            supplier_id=supplier_id
        )
        db.session.add(input_barang)
        db.session.commit()
        
        flash(f'Barang "{nama}" berhasil ditambahkan!', 'success')
        return redirect(url_for('inventory_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menyimpan data: {str(e)}', 'danger')
        return redirect(url_for('inventory_add'))
    
def form_edit(id):
    """Tampilkan form untuk edit barang"""
    try:
        barang = Barang.query.get(id)
        if not barang:
            flash('Data barang tidak ditemukan!', 'warning')
            return redirect(url_for('inventory_index'))
        
        list_kategori = Kategori.query.all()
        list_supplier = Supplier.query.all()
        return render_template('barang/edit.html', 
                             data=barang, 
                             kategori=list_kategori,
                             supplier=list_supplier)
    except Exception as e:
        flash(f'Gagal memuat form edit: {str(e)}', 'danger')
        return redirect(url_for('inventory_index'))

def update(id):
    """Perbarui barang yang ada dengan validasi"""
    try:
        barang = Barang.query.get(id)
        if not barang:
            flash('Data barang tidak ditemukan!', 'warning')
            return redirect(url_for('inventory_index'))
        
        # Ambil data form
        nama = request.form.get('nama_barang', '').strip()
        kode_barang = request.form.get('kode_barang', '').strip()
        harga_beli = request.form.get('harga_beli', 0)
        harga_jual = request.form.get('harga_jual', 0)
        stok = request.form.get('stok', 0)
        stok_minimum = request.form.get('stok_minimum', 10)
        satuan = request.form.get('satuan', 'pcs')
        kategori_id = request.form.get('kategori_id')
        supplier_id = request.form.get('supplier_id') or None
        deskripsi = request.form.get('deskripsi', '')
        
        # Validation
        if not nama:
            flash('Nama barang wajib diisi!', 'warning')
            return redirect(url_for('inventory_edit', id=id))
        
        if not kategori_id:
            flash('Kategori wajib dipilih!', 'warning')
            return redirect(url_for('inventory_edit', id=id))
        
        # Cek apakah kode_barang diubah dan sudah ada
        if kode_barang != barang.kode_barang:
            existing = Barang.query.filter_by(kode_barang=kode_barang).first()
            if existing:
                flash('Kode barang sudah digunakan!', 'warning')
                return redirect(url_for('inventory_edit', id=id))
        
        # Konversi ke tipe data yang sesuai
        try:
            harga_beli = int(harga_beli)
            harga_jual = int(harga_jual)
            stok = int(stok)
            stok_minimum = int(stok_minimum)
        except ValueError:
            flash('Harga dan stok harus berupa angka!', 'warning')
            return redirect(url_for('inventory_edit', id=id))
        
        # Update barang
        barang.kode_barang = kode_barang
        barang.nama_barang = nama
        barang.deskripsi = deskripsi
        barang.harga_beli = harga_beli
        barang.harga_jual = harga_jual
        barang.stok = stok
        barang.stok_minimum = stok_minimum
        barang.satuan = satuan
        barang.kategori_id = kategori_id
        barang.supplier_id = supplier_id
        
        db.session.commit()
        flash(f'Barang "{nama}" berhasil diupdate!', 'success')
        return redirect(url_for('inventory_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal mengupdate data: {str(e)}', 'danger')
        return redirect(url_for('inventory_edit', id=id))

def delete(id):
    """Hapus barang inventory"""
    try:
        barang = Barang.query.get(id)
        if not barang:
            flash('Data barang tidak ditemukan!', 'warning')
            return redirect(url_for('inventory_index'))
        
        nama_barang = barang.nama_barang
        db.session.delete(barang)
        db.session.commit()
        
        flash(f'Barang "{nama_barang}" berhasil dihapus!', 'success')
        return redirect(url_for('inventory_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus data: {str(e)}', 'danger')
        return redirect(url_for('inventory_index'))