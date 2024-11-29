from flask import Blueprint ,jsonify
from utils.mongodb import mongo_room_list, mongo_room_by_id
from typing import Union

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

@room_blueprint.route("/status/<room_id>", methods=["GET"])
def room_latest(room_id: str, q: Union[str, None] = None):
    try:
        rooms = mongo_room_by_id(room_id)
        if rooms:
            return jsonify({"rooms": rooms})
        return jsonify({"status":"NOT FOUND"}), 404
    except Exception as err :
        return jsonify({"status":"ERROR"}), 500