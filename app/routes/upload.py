from flask import Blueprint, jsonify, request, render_template
from ..services.image_service import ImageService
from ..utils.logger import setup_logger

logger = setup_logger()
upload_bp = Blueprint('upload', __name__)

# Will be set when the blueprint is registered
image_service = None

@upload_bp.route('/')
def index():
    return render_template('index.html')

@upload_bp.route('/upload-and-next', methods=['POST'])
def upload_and_next():
    try:
        logger.debug("Received upload request")
        data = request.json
        images = data.get('images', [])
        
        logger.debug(f"Processing {len(images)} images")

        if not images:
            logger.warning("No images provided in request")
            return jsonify({'success': False, 'message': 'No images provided'})

        # Process images and create Shopify listing
        result = image_service.process_images(images)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Successfully created Shopify listing',
                'shopify_product': result['shopify_product']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['error']
            })

    except Exception as e:
        logger.error(f"Error in upload_and_next: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error processing upload: {str(e)}'
        })

def init_upload_routes(openai_client):
    """Initialize the upload routes with dependencies"""
    global image_service
    image_service = ImageService(openai_client) 