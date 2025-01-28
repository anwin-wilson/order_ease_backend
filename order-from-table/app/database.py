from app.models import db

def init_db(app):
    """Initialize database connection."""
    with app.app_context():
        db.create_all()