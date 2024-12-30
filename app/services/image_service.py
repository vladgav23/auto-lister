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

    def process_image(self, image_data):
        """Process a single image to crop it to square"""
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

        # Convert back to base64
        img_byte_arr = io.BytesIO()
        cropped_image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    def generate_metadata(self, images):
        """Generate metadata using OpenAI"""
        if not images:
            raise ValueError("No images provided")

        logger.debug("Processing images")
        # Crop images before sending to OpenAI
        cropped_images = [f"data:image/jpeg;base64,{self.process_image(img)}" for img in images]
        
        logger.debug("Generating metadata using OpenAI")
        listing = Listing.from_base64_list(cropped_images, self.openai_client)
        return listing.get_metadata()

    def create_shopify_listing(self, images, metadata):
        """Create Shopify listing with provided metadata"""
        if not images:
            raise ValueError("No images provided")

        logger.debug("Processing images for Shopify")
        
        # Process images in memory
        processed_images = []
        for image_data in images:
            # Remove the data URL prefix if present
            if 'base64,' in image_data:
                base64_data = image_data.split('base64,')[1]
            else:
                base64_data = image_data

            # Decode base64 to bytes
            image_bytes = base64.b64decode(base64_data)
            processed_images.append(image_bytes)

        # Create Shopify listing
        try:
            shopify_product = self.shopify_service.create_product(
                metadata=metadata,
                image_data=processed_images
            )
            return {
                'success': True,
                'message': 'Listing created successfully'
            }

        except Exception as e:
            logger.error(f"Failed to create Shopify listing: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 