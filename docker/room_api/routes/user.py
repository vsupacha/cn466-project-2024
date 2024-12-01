from flask import Blueprint ,jsonify , render_template
import json
from utils.mongodb import mongo_user_command_list, mongo_get_user_history

user_blueprint = Blueprint('user', __name__)
    
@user_blueprint.route("/list", methods=["GET"])
def user_list():
    users_json = mongo_user_command_list()
    try:
        users = json.loads(users_json)
        if users:
            return render_template('list_user.html', users=users)
        return jsonify({"error": "No users found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding user data"}), 500

@user_blueprint.route("/history/<user_id>", methods=["GET"])
def user_history(user_id: str):
    user_json = mongo_get_user_history(user_id)
    try:
        users = json.loads(user_json)
        if users:
            return render_template('history.html', users=users)
        return jsonify({"error": "User not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding user data"}), 500
    