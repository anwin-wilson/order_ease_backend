from flask import Flask
from flask_cors import CORS
from app.models import db
from app.database import init_db
from app.routes import api

def create_app():
    app = Flask(__name__)
    
    # Database Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:8075028278%40Jio@localhost:5432/restaurant"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize Database
    db.init_app(app)
    
    # Enable CORS
    CORS(app)
    
    # Register Routes
    app.register_blueprint(api, url_prefix="/api")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)