"""Initialize database with default data"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import app, db
from app.model.user import User
from app.model.kategori import Kategori

def init_db():
    """Create tables and insert default data"""
    with app.app_context():
        # Debug: Print database URI (without password)
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        safe_uri = db_uri.replace(os.environ.get('DB_PASSWORD', ''), '****')
        print(f"🔗 Connecting to: {safe_uri}")
        
        # Create all tables
        try:
            db.create_all()
            print("✓ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            print("\n⚠️  Please check:")
            print("   1. MySQL server is running")
            print("   2. Database 'inventory_uas' exists")
            print("   3. .env file is configured correctly")
            return
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create default admin user
            admin = User(
                username='admin',
                email='admin@inventory.com',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Admin user created (username: admin, password: admin123)")
        
        # Create default categories if not exist
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
        
        print("✓ Default categories created")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Database initialization completed!")
        print("\n📝 Default login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Please change the default password after first login!")

if __name__ == '__main__':
    init_db()
