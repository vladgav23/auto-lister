import base64
from PIL import Image
import io
from ..utils.logger import setup_logger
from app.list import Listing
from .shopify_service import ShopifyService
from app.config import Config

logger = setup_logger()

class ImageService:
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.shopify_service = ShopifyService()

    def process_images(self, images):
        """Process images and create Shopify listing"""
        if not images:
            logger.warning("No images provided")
            raise ValueError("No images provided")

        logger.debug("Processing images")
        
        # Process images in memory
        processed_images = []
        for i, image_data in enumerate(images):
            logger.debug(f"Processing image {i+1}")
            
            # Remove the data URL prefix if present
            if 'base64,' in image_data:
                base64_data = image_data.split('base64,')[1]
            else:
                base64_data = image_data

            # Decode base64 to image
            image_bytes = base64.b64decode(base64_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Calculate dimensions for square crop
            width, height = image.size
            size = min(width, height)
            
            # Calculate coordinates for center crop
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size

            # Crop the image
            cropped_image = image.crop((left, top, right, bottom))

            # Convert back to bytes
            img_byte_arr = io.BytesIO()
            cropped_image.save(img_byte_arr, format='JPEG')
            processed_images.append(img_byte_arr.getvalue())

        # Generate metadata using the Listing class
        logger.debug("Generating listing metadata")
        listing = Listing.from_base64_list(images, self.openai_client)
        metadata = listing.get_metadata()

        # Create Shopify listing
        try:
            shopify_product = self.shopify_service.create_product(
                metadata=metadata,
                image_data=processed_images
            )
            return {
                'success': True,
                'shopify_product': {
                    'title': shopify_product.title,
                    'description': shopify_product.body_html,
                    'price': shopify_product.variants[0].price if shopify_product.variants else None,
                    'category': shopify_product.product_type,
                    'tags': shopify_product.tags,
                    'url': f"https://{Config.SHOPIFY_SHOP_URL}/products/{shopify_product.handle}",
                    'images': [img.src for img in shopify_product.images] if hasattr(shopify_product, 'images') else []
                }
            }

        except Exception as e:
            logger.error(f"Failed to create Shopify listing: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 