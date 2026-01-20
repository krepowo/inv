from app.model.kategori import Kategori
from app import db
from flask import render_template, request, redirect, url_for, flash

def index():
    """Display all categories"""
    try:
        data = Kategori.query.order_by(Kategori.nama_kategori).all()
        return render_template('kategori_index.html', data=data)
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return render_template('kategori_index.html', data=[])

def form_tambah():
    """Display form to add new category"""
    return render_template('kategori_tambah.html')

def save():
    """Save new category with validation"""
    try:
        nama = request.form.get('nama_kategori', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        
        # Validation
        if not nama:
            flash('Nama kategori wajib diisi!', 'warning')
            return redirect(url_for('kategori_add'))
        
        # Check if category already exists
        existing = Kategori.query.filter_by(nama_kategori=nama).first()
        if existing:
            flash('Kategori dengan nama tersebut sudah ada!', 'warning')
            return redirect(url_for('kategori_add'))
        
        kategori_baru = Kategori(nama_kategori=nama, deskripsi=deskripsi)
        db.session.add(kategori_baru)
        db.session.commit()
        
        flash(f'Kategori "{nama}" berhasil ditambahkan!', 'success')
        return redirect(url_for('kategori_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menyimpan kategori: {str(e)}', 'danger')
        return redirect(url_for('kategori_add'))
    
def form_edit(id):
    """Display form to edit category"""
    try:
        kategori = Kategori.query.get(id)
        if not kategori:
            flash('Kategori tidak ditemukan!', 'warning')
            return redirect(url_for('kategori_index'))
        return render_template('kategori_edit.html', data=kategori)
    except Exception as e:
        flash(f'Gagal memuat form: {str(e)}', 'danger')
        return redirect(url_for('kategori_index'))

def update(id):
    """Update existing category with validation"""
    try:
        kategori = Kategori.query.get(id)
        if not kategori:
            flash('Kategori tidak ditemukan!', 'warning')
            return redirect(url_for('kategori_index'))
        
        nama = request.form.get('nama_kategori', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        
        # Validation
        if not nama:
            flash('Nama kategori wajib diisi!', 'warning')
            return redirect(url_for('kategori_edit', id=id))
        
        # Check if category name already exists (excluding current)
        existing = Kategori.query.filter(
            Kategori.nama_kategori == nama,
            Kategori.id != id
        ).first()
        if existing:
            flash('Kategori dengan nama tersebut sudah ada!', 'warning')
            return redirect(url_for('kategori_edit', id=id))
        
        kategori.nama_kategori = nama
        kategori.deskripsi = deskripsi
        db.session.commit()
        
        flash(f'Kategori "{nama}" berhasil diupdate!', 'success')
        return redirect(url_for('kategori_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal update kategori: {str(e)}', 'danger')
        return redirect(url_for('kategori_edit', id=id))

def delete(id):
    """Delete category"""
    try:
        kategori = Kategori.query.get(id)
        if not kategori:
            flash('Kategori tidak ditemukan!', 'warning')
            return redirect(url_for('kategori_index'))
        
        # Check if category has items
        if kategori.barang.count() > 0:
            flash('Tidak dapat menghapus kategori yang masih memiliki barang!', 'danger')
            return redirect(url_for('kategori_index'))
        
        nama_kategori = kategori.nama_kategori
        db.session.delete(kategori)
        db.session.commit()
        
        flash(f'Kategori "{nama_kategori}" berhasil dihapus!', 'success')
        return redirect(url_for('kategori_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal hapus kategori: {str(e)}', 'danger')
        return redirect(url_for('kategori_index'))