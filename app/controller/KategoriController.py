from app.model.kategori import Kategori
from app import db
from flask import render_template, request, redirect, url_for

def index():
    # Menampilkan semua kategori
    data = Kategori.query.all()
    return render_template('kategori_index.html', data=data)

def form_tambah():
    # Menampilkan form
    return render_template('kategori_tambah.html')

def save():
    # Menyimpan data kategori baru
    try:
        nama = request.form.get('nama_kategori')
        if nama:
            kategori_baru = Kategori(nama_kategori=nama)
            db.session.add(kategori_baru)
            db.session.commit()
            return redirect(url_for('kategori_index'))
    except Exception as e:
        print(e)
        return "Gagal menyimpan kategori"
    
def form_edit(id):
    kategori = Kategori.query.get(id)
    return render_template('kategori_edit.html', data=kategori)

def update(id):
    try:
        kategori = Kategori.query.get(id)
        if kategori:
            kategori.nama_kategori = request.form.get('nama_kategori')
            db.session.commit()
        return redirect(url_for('kategori_index'))
    except Exception as e:
        print(e)
        return "Gagal update kategori"

def delete(id):
    try:
        kategori = Kategori.query.get(id)
        if kategori:
            db.session.delete(kategori)
            db.session.commit()
        return redirect(url_for('kategori_index'))
    except Exception as e:
        print(e)
        return "Gagal hapus kategori"