import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'udb'
    
    HOST = os.environ.get("DB_HOST", "localhost")
    DATABASE = os.environ.get("DB_DATABASE", "inventory_uas")
    USERNAME = os.environ.get("DB_USERNAME", "root")
    PASSWORD = os.environ.get("DB_PASSWORD", "")
    
    # Construct database URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Debug config (remove in production)
    @staticmethod
    def init_app(app):
        # Print config for debugging (hide password)
        safe_uri = Config.SQLALCHEMY_DATABASE_URI.replace(Config.PASSWORD, '****')
        print(f"📊 Database: {safe_uri}")