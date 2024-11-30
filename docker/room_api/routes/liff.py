from flask import request, Blueprint, render_template, jsonify
from utils.mongodb import mongo_room_list, mongo_room_by_id, mongo_user_command_list, mongo_get_user_history
import json

liff_blueprint = Blueprint('liff', __name__, template_folder='../templates', static_folder='../static')

@liff_blueprint.route("/")
def liff():
    room_list = json.loads(mongo_room_list())
    rooms = [item['room_id'] for item in room_list]
    result = [{"room_id": item["room_id"], "status": item["status"]} for item in room_list]
    return render_template('list_room.html', rooms=rooms, result=result)

@liff_blueprint.route("/status")
def get_data():
    room_id = request.args.get("room_id", "OverAll")
    room_list = json.loads(mongo_room_list())
    rooms = [item['room_id'] for item in room_list]
    try:
        if room_id == 'OverAll':
            room_list = json.loads(mongo_room_list())
            result = [{"room_id": item["room_id"], "status": item["status"]} for item in room_list]
            return render_template('list_room.html', rooms=rooms, result=result)
        else :
            room = json.loads(mongo_room_by_id(room_id))
            result = [{"room_id": item["room_id"], "status": item["status"]} for item in room]
            return render_template('list_room.html', rooms=rooms, result=result)
    except Exception as err :
        result = [{"status":"ERROR"}]
        return render_template('list_room.html', rooms=rooms, result=result)
    
@liff_blueprint.route("/list", methods=["GET"])
def user_list():
    users_json = mongo_user_command_list()
    try:
        users = json.loads(users_json)
        if users:
            return render_template('list_user.html', users=users)
        return jsonify({"error": "No users found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding user data"}), 500

@liff_blueprint.route("/history/<user_id>", methods=["GET"])
def user_history(user_id: str):
    user_json = mongo_get_user_history(user_id)
    try:
        users = json.loads(user_json)
        if users:
            return render_template('history.html', users=users)
        return jsonify({"error": "User not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding user data"}), 500
