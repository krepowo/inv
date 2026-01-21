from app import db
from datetime import datetime

class Kategori(db.Model):
    __tablename__ = 'kategori'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_kategori = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relasi
    barang = db.relationship('Barang', backref='kategori', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return '<Kategori {}>'.format(self.nama_kategori)