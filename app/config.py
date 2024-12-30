import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    UPLOAD_FOLDER = 'uploads'
    
    # Shopify configuration
    SHOPIFY_SHOP_URL = os.getenv('SHOPIFY_SHOP_URL')
    SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
    SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
    SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
    
    @staticmethod
    def init_app(app):
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER) 