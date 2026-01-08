from app import db
from app.model.kategori import Kategori

class Barang(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_barang = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)
    kategori_id = db.Column(db.BigInteger, db.ForeignKey(Kategori.id, ondelete='CASCADE'))
    
    def __repr__(self):
        return '<Barang {}>'.format(self.nama_barang)