from flask import Flask
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class='config.DevelopmentConfig'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app)
    
    # Set up logging
    setup_logging(app)
    
    # Initialize database connection
    from .dataAccessLayer import init_db
    init_db(app)
    
    # Register blueprints
    from .routes import api
    app.register_blueprint(api, url_prefix="/api")
    
    return app

def setup_logging(app):
    """Set up logging for the application."""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/myapp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('MyApp startup')