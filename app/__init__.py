from flask import Flask
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def create_app(config_name='development'):
    """Application factory"""
    # Get absolute paths for template and static folders
    app_dir = Path(__file__).parent
    template_folder = str(app_dir / 'templates')
    static_folder = str(app_dir / 'static')
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    
    # Load configuration
    from config import config
    if config_name in config:
        config_obj = config[config_name]
        if hasattr(config_obj, '__dict__'):
            app.config.update({k: v for k, v in config_obj.__dict__.items() if not k.startswith('_')})
        else:
            app.config.update(config_obj)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
