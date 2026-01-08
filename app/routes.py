from flask import request 

from app import app
from app.controller import InventoryController
from app.controller import KategoriController

@app.route('/')
def inventory_index():
    return InventoryController.index()

# CRUD Inventory
@app.route('/tambah', methods=['GET', 'POST'])
def inventory_add():
    if request.method == 'GET':
        return InventoryController.form_tambah()
    else:
        return InventoryController.save()
@app.route('/edit/<id>', methods=['GET'])
def inventory_edit(id):
    return InventoryController.form_edit(id)

@app.route('/update/<id>', methods=['POST'])
def inventory_update(id):
    return InventoryController.update(id)

@app.route('/hapus/<id>')
def inventory_delete(id):
    return InventoryController.delete(id)

# CRUD Kategori
@app.route('/kategori')
def kategori_index():
    return KategoriController.index()

@app.route('/kategori/tambah', methods=['GET', 'POST'])
def kategori_add():
    if request.method == 'GET':
        return KategoriController.form_tambah()
    else:
        return KategoriController.save()
@app.route('/kategori/edit/<id>', methods=['GET'])
def kategori_edit(id):
    return KategoriController.form_edit(id)

@app.route('/kategori/update/<id>', methods=['POST'])
def kategori_update(id):
    return KategoriController.update(id)

@app.route('/kategori/hapus/<id>')
def kategori_delete(id):
    return KategoriController.delete(id)