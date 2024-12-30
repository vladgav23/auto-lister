from flask import Flask, render_template, request, jsonify, send_from_directory
import logging
import os
import base64
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from list import Listing

# Load environment variables and initialize OpenAI client
load_dotenv()
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add debug flag
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

if DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug mode enabled")

# Initialize Flask app with static and template folders
app = Flask(__name__,
    static_folder='static',
    template_folder='templates'
)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Track current batch
current_batch = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-and-next', methods=['POST'])
def upload_and_next():
    try:
        logger.debug("Received upload-and-next request")
        data = request.json
        batch_num = data.get('currentBatch', current_batch)
        images = data.get('images', [])
        
        logger.debug(f"Processing batch {batch_num} with {len(images)} images")

        if not images:
            logger.warning("No images provided in request")
            return jsonify({'success': False, 'message': 'No images provided'})

        # Create batch directory if it doesn't exist
        batch_dir = os.path.join(UPLOAD_FOLDER, f'batch_{batch_num}')
        if not os.path.exists(batch_dir):
            os.makedirs(batch_dir)

        logger.debug(f"Created batch directory: {batch_dir}")

        # Save images to disk
        saved_paths = []
        for i, image_data in enumerate(images):
            logger.debug(f"Processing image {i+1}")
            # Remove the data URL prefix if present
            if 'base64,' in image_data:
                base64_data = image_data.split('base64,')[1]
            else:
                base64_data = image_data

            # Generate unique filename using timestamp and index
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'photo_{timestamp}_{i+1}.jpg'
            filepath = os.path.join(batch_dir, filename)

            # Save the image
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(base64_data))
            saved_paths.append(filepath)

            logger.debug(f"Saved image to {filepath}")

        logger.debug("Generating listing metadata")
        listing = Listing.from_base64_list(images, openai_client)
        metadata = listing.get_metadata()
        
        # Convert Pydantic model to dictionary and ensure JSON serializable
        metadata_dict = json.loads(json.dumps(metadata.model_dump()))

        logger.debug(f"Generated metadata: {metadata_dict}")

        # Save metadata to a file in the batch directory
        metadata_path = os.path.join(batch_dir, 'metadata.txt')
        with open(metadata_path, 'w') as f:
            json.dump(metadata_dict, f)
        
        return jsonify({
            'success': True,
            'message': f'{len(images)} images uploaded to batch {batch_num}',
            'metadata': metadata_dict,
            'nextBatch': batch_num + 1
        })

    except Exception as e:
        logger.error(f"Error in upload_and_next: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error processing upload: {str(e)}'
        })

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'success': False,
        'message': 'File too large'
    }), 413

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Use adhoc SSL context for HTTPS (required for camera access)
    app.run(host='0.0.0.0', port=5001, ssl_context='adhoc')