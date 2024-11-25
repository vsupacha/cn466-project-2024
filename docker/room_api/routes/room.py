from flask import Blueprint
from utils.mongodb import mongo_room_list

# Initialize the blueprint for image handling
room_blueprint = Blueprint('room', __name__)

# View image route
@room_blueprint.route("/list", methods=["GET"])
def room_list():
    rooms = mongo_room_list()
    return rooms