from app import db
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'supplier'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_supplier = db.Column(db.String(100), nullable=False)
    kontak_supplier = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    alamat = db.Column(db.Text, nullable=True)
    keterangan = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    barang = db.relationship('Barang', backref='supplier', lazy='dynamic')
    transaksi = db.relationship('Transaksi', backref='supplier', lazy='dynamic')
    
    def __repr__(self):
        return '<Supplier {}>'.format(self.nama_supplier)