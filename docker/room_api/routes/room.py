from flask import Blueprint ,jsonify
from utils.mongodb import mongo_room_list

# Initialize the blueprint for image handling
room_blueprint = Blueprint('room', __name__)

# Routes
@room_blueprint.route("/list", methods=["GET"])
def room_list():
    """Fetch all rooms."""
    rooms = mongo_room_list()
    if rooms:
        return jsonify({"rooms": rooms})
    return jsonify({"error": "No rooms found"}), 404