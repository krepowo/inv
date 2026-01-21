from app import db
from datetime import datetime

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    kode_transaksi = db.Column(db.String(50), unique=True, nullable=False)
    tipe_transaksi = db.Column(db.String(10), nullable=False)  # 'masuk' atau 'keluar'
    barang_id = db.Column(db.BigInteger, db.ForeignKey('barang.id', ondelete='CASCADE'), nullable=False)
    supplier_id = db.Column(db.BigInteger, db.ForeignKey('supplier.id', ondelete='SET NULL'), nullable=True)
    jumlah = db.Column(db.Integer, nullable=False)
    harga_satuan = db.Column(db.Integer, nullable=False, default=0)
    total_harga = db.Column(db.Integer, nullable=False, default=0)
    keterangan = db.Column(db.Text, nullable=True)
    tanggal_transaksi = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_total(self):
        """Hitung total harga berdasarkan jumlah dan harga satuan"""
        self.total_harga = self.jumlah * self.harga_satuan
    
    def __repr__(self):
        return '<Transaksi {}>'.format(self.kode_transaksi)
