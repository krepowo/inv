from app import db
from datetime import datetime

class Barang(db.Model):
    __tablename__ = 'barang'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    kode_barang = db.Column(db.String(50), unique=True, nullable=False)
    nama_barang = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    harga_beli = db.Column(db.Integer, nullable=False, default=0)
    harga_jual = db.Column(db.Integer, nullable=False, default=0)
    stok = db.Column(db.Integer, nullable=False, default=0)
    stok_minimum = db.Column(db.Integer, nullable=False, default=10)
    satuan = db.Column(db.String(20), nullable=False, default='pcs')
    kategori_id = db.Column(db.BigInteger, db.ForeignKey('kategori.id', ondelete='CASCADE'))
    supplier_id = db.Column(db.BigInteger, db.ForeignKey('supplier.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relasi
    transaksi = db.relationship('Transaksi', backref='barang', lazy='dynamic')
    
    def is_low_stock(self):
        """Cek apakah stok di bawah batas minimum"""
        return self.stok <= self.stok_minimum
    
    def update_stok(self, jumlah, tipe):
        """Perbarui stok berdasarkan tipe transaksi"""
        if tipe == 'masuk':
            self.stok += jumlah
        elif tipe == 'keluar':
            if self.stok >= jumlah:
                self.stok -= jumlah
            else:
                raise ValueError('Stok tidak mencukupi')
    
    def __repr__(self):
        return '<Barang {}>'.format(self.nama_barang)