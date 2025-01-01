from pydantic import BaseModel
from PIL import Image
import pillow_heif
import os
import io
import base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import logging
from app.config import Config

logger = logging.getLogger(__name__)


class ListingMetadata(BaseModel):
    title: str
    description: str
    category: str
    tags: list[str]
    estimated_price: int


class Listing:
    def __init__(self, openai_client):
        self.client = openai_client
        logger.debug("Initialized new Listing instance")

    @classmethod
    def from_directory(cls, img_dir, openai_client):
        logger.debug(f"Creating Listing from directory: {img_dir}")
        instance = cls(openai_client)
        instance.images = cls._load_images_from_directory(img_dir)
        logger.debug(f"Loaded {len(instance.images)} images from directory")
        return instance

    @classmethod
    def from_base64_list(cls, base64_images, openai_client):
        logger.debug(f"Creating Listing from {len(base64_images)} base64 images")
        instance = cls(openai_client)
        instance.images = cls._prepare_base64_images(base64_images)
        logger.debug("Finished preparing base64 images")
        return instance

    @staticmethod
    def _prepare_base64_images(base64_images):
        logger.debug("Starting base64 image preparation")
        images = []
        for i, img_data in enumerate(base64_images):
            logger.debug(f"Processing base64 image {i+1}")
            # Ensure the image data has the proper data URL format
            if not img_data.startswith('data:image'):
                img_data = f'data:image/jpeg;base64,{img_data}'

            images.append({
                "type": "image_url",
                "image_url": {
                    "url": img_data
                }
            })
        logger.debug(f"Prepared {len(images)} images")
        return images

    @staticmethod
    def _load_images_from_directory(img_dir):
        logger.debug(f"Loading images from directory: {img_dir}")
        pillow_heif.register_heif_opener()
        images = []
        image_files = list(Path(img_dir).glob('*.HEIC')) + \
                      list(Path(img_dir).glob('*.heic')) + \
                      list(Path(img_dir).glob('*.jpg')) + \
                      list(Path(img_dir).glob('*.jpeg')) + \
                      list(Path(img_dir).glob('*.png'))
        
        logger.debug(f"Found {len(image_files)} image files")

        for img_path in image_files:
            try:
                logger.debug(f"Processing image: {img_path}")
                image = Image.open(img_path)
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                images.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })
                logger.debug(f"Successfully processed {img_path}")
            except Exception as e:
                logger.error(f"Error loading {img_path}: {str(e)}", exc_info=True)

        return images

    def get_metadata(self):
        logger.debug("Getting metadata from OpenAI")
        messages = [
            {"role": "system", "content": Config.PRICING_ANALYST_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": "Please analyze these images and provide a valuation for the items shown."},
                *self.images
            ]}
        ]

        logger.debug("Sending request to OpenAI")
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=ListingMetadata,
            temperature=0
        )
        logger.debug("Received response from OpenAI")

        return completion.choices[0].message.parsed


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    # Process all folders in data directory
    data_folders = [d for d in Path("data").iterdir() if d.is_dir()]

    for folder in data_folders:
        try:
            listing = Listing.from_directory(str(folder), client)
            print(f"\n=== {folder.name} ===")
            print(listing.get_metadata())
        except Exception as e:
            print(f"Error processing {folder.name}: {e}")