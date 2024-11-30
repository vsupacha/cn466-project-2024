
from flask import Blueprint ,jsonify , request
from utils.mongodb import mongo_user_command_list, mongo_get_user_command
from typing import Union


# Initialize the blueprint for image handling
user_blueprint = Blueprint('user', __name__)

# Routes
@user_blueprint.route("/list", methods=["GET"])
def user_list():
    """Fetch all users."""
    users = mongo_user_command_list()
    if users:
        return jsonify({"users": users})
    return jsonify({"error": "No users found"}), 404

@user_blueprint.route("/command/<user_id>", methods=["GET"])
def command_latest(user_id: str, q: Union[str, None] = None):
    try:
        user = mongo_get_user_command(user_id)
        if user:
            return jsonify({"user": user})
        return jsonify({"status":"NOT FOUND"}), 404
    except Exception as err :
        return jsonify({"status":"ERROR"}), 500
    
# @user_blueprint.route("/event", methods=["GET"])
# def user_event():
#     user_id = request.args.get("id")
#     condition = int(request.args.get("condition"))
#     try:
#         event_data = mongo_room_event(user_id,condition)
#         if event_data:
#             return jsonify({
#                 "status":"SUCCESS",
#                 "event": event_data})
#         return jsonify({"status":"NOT FOUND"}), 404
#     except Exception as err :
#         return jsonify({"status":"ERROR"}), 500
    
