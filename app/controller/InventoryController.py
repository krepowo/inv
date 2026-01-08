from app.model.barang import Barang
from app.model.kategori import Kategori
from app import db
from flask import render_template, request, redirect, url_for

def index():
    # Mengambil semua data barang gabung dengan kategori
    list_barang = db.session.query(Barang, Kategori).join(Kategori).all()
    return render_template('index.html', data=list_barang)

def form_tambah():
    # Menampilkan form tambah dengan data kategori untuk dropdown
    list_kategori = Kategori.query.all()
    return render_template('tambah.html', kategori=list_kategori)

def save():
    try:
        nama = request.form.get('nama_barang')
        harga = request.form.get('harga')
        stok = request.form.get('stok')
        kategori_id = request.form.get('kategori_id')
        
        input_barang = Barang(nama_barang=nama, harga=harga, stok=stok, kategori_id=kategori_id)
        db.session.add(input_barang)
        db.session.commit()
        
        return redirect(url_for('inventory_index'))
    except Exception as e:
        print(e)
        return "Gagal menyimpan data"
    
def form_edit(id):
    # cari dari id
    barang = Barang.query.get(id)
    list_kategori = Kategori.query.all()
    if not barang:
        return "Data tidak ditemukan"
    return render_template('edit.html', data=barang, kategori=list_kategori)

def update(id):
    try:
        barang = Barang.query.get(id)
        if barang:
            barang.nama_barang = request.form.get('nama_barang')
            barang.harga = request.form.get('harga')
            barang.stok = request.form.get('stok')
            barang.kategori_id = request.form.get('kategori_id')
            
            db.session.commit()
            return redirect(url_for('inventory_index'))
    except Exception as e:
        print(e)
        return "Gagal mengupdate data"

def delete(id):
    try:
        barang = Barang.query.get(id)
        if barang:
            db.session.delete(barang)
            db.session.commit()
        return redirect(url_for('inventory_index'))
    except Exception as e:
        print(e)
        return "Gagal menghapus data"