from flask import Blueprint, request, jsonify, send_from_directory
import os
import uuid
import time
from utils.mongodb import mongo_room_list

# Initialize the blueprint for image handling
room_blueprint = Blueprint('room', __name__)

# View image route
@room_blueprint.route("/list", methods=["GET"])
def show_image(uuid):
    rooms = mongo_room_list()
    return rooms