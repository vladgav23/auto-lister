from flask import Flask, jsonify
from .config import Config
from .routes.upload import upload_bp
from openai import OpenAI

openai_client = None

def create_app(config_class=Config):
    app = Flask(__name__,
        static_folder='static',
        template_folder='templates'
    )
    
    app.config.from_object(config_class)
    
    global openai_client
    openai_client = OpenAI(api_key=config_class.OPENAI_API_KEY)
    
    # Initialize routes with dependencies
    from .routes.upload import init_upload_routes
    init_upload_routes(openai_client)
    
    # Register blueprints
    app.register_blueprint(upload_bp)
    
    # Register error handlers
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'success': False, 'message': 'File too large'}), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
        
    return app 