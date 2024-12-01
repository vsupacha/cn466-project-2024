from flask import Blueprint ,jsonify
import json
from typing import Union
from utils.mongodb import mongo_user_command_list, mongo_get_user_command

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
    