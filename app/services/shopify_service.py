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
            
            # Handle required fields
            new_product.title = metadata.get('title', '')
            new_product.body_html = metadata.get('description', '')
            new_product.vendor = "Butler Warehouse"
            new_product.product_type = metadata.get('category', '')
            
            # Handle tags - ensure it's a list
            tags = metadata.get('tags', [])
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',')]
            new_product.tags = tags
            
            # Create a variant with the price
            variant = shopify.Variant({
                'price': str(metadata.get('price', 0))  # Changed from estimated_price to price
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