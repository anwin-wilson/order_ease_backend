from flask import Blueprint, jsonify, request, Flask
from flask_cors import CORS
from .dataAccessLayer import MyApp
from http import HTTPStatus
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint for API routes
api = Blueprint("api", __name__)

# Initialize the data access layer
my_app = MyApp()

@api.route("/categories", methods=["GET"])
def get_categories():
    """
    Fetch all categories.
    """
    try:
        categories = my_app.get_all_categories()
        if not categories:
            logger.info("No categories found.")
            return jsonify({"message": "No categories found"}), HTTPStatus.NOT_FOUND

        result = [{"category_id": c.category_id, "name": c.name} for c in categories]
        logger.info(f"Fetched {len(result)} categories.")
        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify({"message": "An error occurred while fetching categories."}), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/categories/<int:category_id>/dishes", methods=["GET"])
def get_dishes(category_id):
    """
    Fetch dishes by category ID.
    """
    try:
        # Validate category_id (Optional if database handles this)
        if category_id <= 0:
            logger.warning(f"Invalid category ID: {category_id}")
            return jsonify({"message": "Invalid category ID"}), HTTPStatus.BAD_REQUEST

        dishes = my_app.get_dishes_by_category_id(category_id)
        if not dishes:
            logger.info(f"No dishes found for category ID: {category_id}")
            return jsonify({"message": f"No dishes found for category {category_id}"}), HTTPStatus.NOT_FOUND

        result = [
            {
                "menu_item_id": d.menu_item_id,
                "name": d.name,
                "description": d.description,
                "price": str(d.price),  # Ensuring price is string for JSON compatibility
                "is_available": d.is_available,
            }
            for d in dishes
        ]
        logger.info(f"Fetched {len(result)} dishes for category ID: {category_id}")
        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error fetching dishes for category {category_id}: {e}")
        return jsonify({"message": "An error occurred while fetching dishes."}), HTTPStatus.INTERNAL_SERVER_ERROR

@api.route("/order_items", methods=["POST"])
def add_order_item():
    """
    Add an order item.
    """
    try:
        data = request.get_json()
        menu_item_id = data.get("menu_item_id")
        quantity = data.get("quantity")
        order_id = data.get("order_id")
        price = data.get("price")

        # Validate required fields
        if not menu_item_id or not quantity or not order_id or price is None:
            logger.warning("Missing or invalid required fields in request data.")
            return jsonify({"message": "Missing or invalid required fields"}), HTTPStatus.BAD_REQUEST

        # Ensure numeric fields are correctly formatted
        try:
            menu_item_id = int(menu_item_id)
            quantity = int(quantity)
            order_id = int(order_id)
            price = float(price)
        except ValueError as e:
            logger.warning(f"Invalid data type: {e}")
            return jsonify({"message": "Invalid data types for fields"}), HTTPStatus.BAD_REQUEST

        order_item = my_app.add_order_item(menu_item_id, quantity, order_id, price)
        logger.info(f"Added order item with ID: {order_item.order_item_id}")
        return jsonify({"message": "Order item added successfully", "order_item_id": order_item.order_item_id}), HTTPStatus.CREATED

    except Exception as e:
        logger.error(f"Error adding order item: {e}")
        return jsonify({"message": "An error occurred while adding the order item."}), HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as e:
        logger.error(f"Error adding order item: {e}")
        return jsonify({"message": "An error occurred while adding the order item."}), HTTPStatus.INTERNAL_SERVER_ERROR