"""Inisialisasi database dengan data default"""
import os
from dotenv import load_dotenv

# Load variabel environment dari file .env
load_dotenv()

from app import app, db
from app.model.user import User
from app.model.kategori import Kategori

def init_db():
    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        safe_uri = db_uri.replace(os.environ.get('DB_PASSWORD', ''), '****')
        
        try:
            db.create_all()
            print("✓ Berhasil membuat semua tabel!")
        except Exception as e:
            print(f"❌ Gagal membuat tabel: {e}")
            print("\n⚠️  Silakan periksa:")
            print("   1. Pastikan XAMPP/Laragon nyala")
            print("   2. Database bernama'inventory_uas' ada")
            
            return
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@gmail.com',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Admin user dibuat (username: admin, password: admin123)")
        
        default_categories = [
            {'nama': 'Elektronik', 'desc': 'Barang elektronik dan gadget'},
            {'nama': 'Furniture', 'desc': 'Furniture dan perlengkapan kantor'},
            {'nama': 'ATK', 'desc': 'Alat Tulis Kantor'},
            {'nama': 'Makanan & Minuman', 'desc': 'Produk makanan dan minuman'},
            {'nama': 'Pakaian', 'desc': 'Pakaian dan aksesoris'},
        ]
        
        for cat_data in default_categories:
            existing = Kategori.query.filter_by(nama_kategori=cat_data['nama']).first()
            if not existing:
                kategori = Kategori(
                    nama_kategori=cat_data['nama'],
                    deskripsi=cat_data['desc']
                )
                db.session.add(kategori)
        
        print("✓ Kategori default berhasil dibuat")
        
        db.session.commit()
        print("\n✅ Setup database selesai!")
        print("\n📝 Info login admin:")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == '__main__':
    init_db()
