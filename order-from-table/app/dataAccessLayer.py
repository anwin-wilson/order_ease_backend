from .models import db, Category, MenuItem, OrderItem
import logging
from .db import DatabaseHandler
from typing import List

logger = logging.getLogger(__name__)
db_handler = None

def init_db(app):
    """Initialize database connection."""
    global db_handler
    db_handler = DatabaseHandler(app.config['SQLALCHEMY_DATABASE_URI'])

class MyApp:
    def __init__(self):
        self.db_handler = db_handler
        logger.info("MyApp startup")

    def get_all_categories(self) -> List[Category]:
        """Get all categories."""
        return Category.query.all()

    def get_dishes_by_category_id(self, category_id: int) -> List[MenuItem]:
        """Get dishes by category ID."""
        return MenuItem.query.filter_by(category_id=category_id, is_available=True).all()

    def add_order_item(self, menu_item_id: int, quantity: int, order_id: int, price: float) -> OrderItem:
        """Add an order item."""
        if price is None:
            raise ValueError("Price cannot be None.")

        order_item = OrderItem(menu_item_id=menu_item_id, quantity=quantity, order_id=order_id, price=price)
        db.session.add(order_item)
        db.session.commit()
        return order_item


    def __del__(self):
        if self.db_handler:
            try:
                self.db_handler.close_pool()
            except AttributeError:
                logger.error("DatabaseHandler object has no attribute 'close_pool'")