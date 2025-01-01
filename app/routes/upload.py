from flask import Blueprint, jsonify, request, render_template, Response
from functools import wraps
from ..config import Config
from ..services.image_service import ImageService
from ..utils.logger import setup_logger

logger = setup_logger()
upload_bp = Blueprint('upload', __name__)

# Will be set when the blueprint is registered
image_service = None

def check_auth(username, password):
    """Check if the password matches"""
    return password == Config.AUTH_PASSWORD

def authenticate():
    """Send a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@upload_bp.route('/')
@requires_auth
def index():
    return render_template('index.html')

@upload_bp.route('/generate-metadata', methods=['POST'])
@requires_auth
def generate_metadata():
    try:
        logger.debug("Received metadata generation request")
        data = request.json
        images = data.get('images', [])
        
        if not images:
            logger.warning("No images provided in request")
            return jsonify({'success': False, 'message': 'No images provided'})

        # Generate metadata using OpenAI and get cropped images
        metadata = image_service.generate_metadata(images)
        
        # Get cropped images
        cropped_images = [f"data:image/jpeg;base64,{image_service.process_image(img)}" for img in images]
        
        # Convert Pydantic model to dict
        metadata_dict = metadata.model_dump()
        
        return jsonify({
            'success': True,
            'metadata': metadata_dict,
            'cropped_images': cropped_images
        })

    except Exception as e:
        logger.error(f"Error generating metadata: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error generating metadata: {str(e)}'
        })

@upload_bp.route('/create-listing', methods=['POST'])
@requires_auth
def create_listing():
    try:
        logger.debug("Received create listing request")
        data = request.json
        images = data.get('images', [])
        metadata = data.get('metadata')
        
        logger.debug(f"Received metadata: {metadata}")
        
        if not images or not metadata:
            return jsonify({'success': False, 'message': 'Missing images or metadata'})

        # Create Shopify listing with the provided metadata
        result = image_service.create_shopify_listing(images, metadata)
        
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error creating listing: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error creating listing: {str(e)}'
        })

def init_upload_routes(openai_client):
    """Initialize the upload routes with dependencies"""
    global image_service
    image_service = ImageService(openai_client) 