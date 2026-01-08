from app import db

class Kategori(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_kategori = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Kategori {}>'.format(self.nama_kategori)