# import requests
import shopify
from ..config import Config
from ..utils.logger import setup_logger
import certifi
import ssl
import urllib3
import base64

logger = setup_logger()

class ShopifyService:
    def __init__(self):
        # Disable SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Create SSL context with certifi
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Set default SSL cert path
        ssl._create_default_https_context = ssl._create_unverified_context

    def create_product(self, metadata, image_data):
        with shopify.Session.temp(Config.SHOPIFY_SHOP_URL, '2024-01', Config.SHOPIFY_ACCESS_TOKEN) as session:
            new_product = shopify.Product()
            new_product.title = metadata.title
            new_product.body_html = metadata.description
            new_product.vendor = "Butler Warehouse"
            new_product.product_type = metadata.category
            new_product.tags = metadata.tags
            
            # Create a variant with the price and proper inventory settings
            variant = shopify.Variant({
                'price': str(metadata.estimated_price)
            })
            new_product.variants = [variant]
            
            # First save the product to get an ID
            success = new_product.save()
            
            if success:
                # Now attach images to the saved product
                for img_data in image_data:
                    image = shopify.Image()
                    image.product_id = new_product.id
                    image.attachment = base64.b64encode(img_data).decode('utf-8')
                    image.save()
                        
                # Reload the product to get the updated data with images
                new_product.reload()
            else:
                logger.error("Failed to create Shopify product")
                raise Exception("Failed to create Shopify product")

        return new_product