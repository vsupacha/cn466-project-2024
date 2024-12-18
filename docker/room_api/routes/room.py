from flask import Blueprint ,jsonify , request
from utils.mongodb import mongo_room_list, mongo_room_by_id, mongo_room_event
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
    
@room_blueprint.route("/event", methods=["GET"])
def room_event():
    room_id = request.args.get("id")
    condition = int(request.args.get("condition"))
    try:
        event_data = mongo_room_event(room_id,condition)
        if event_data:
            return jsonify({
                "status":"SUCCESS",
                "event": event_data})
        return jsonify({"status":"NOT FOUND"}), 404
    except Exception as err :
        return jsonify({"status":"ERROR"}), 500
