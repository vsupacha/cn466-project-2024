from flask import request, abort, Blueprint, render_template, jsonify
from utils.mongodb import mongo_room_list, mongo_room_by_id
from typing import Union
import json

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

liff_blueprint = Blueprint('liff', __name__, template_folder='../templates')
liff_id = '2006527696-Xkd3WNLr'

@liff_blueprint.route("/")
def liff():
    room_list = json.loads(mongo_room_list())
    rooms = [item['room_id'] for item in room_list]
    result = [{"room_id": item["room_id"], "status": item["status"]} for item in room_list]
    return render_template('list_room.html', liff_id=liff_id, rooms=rooms, result=result)

@liff_blueprint.route("/status")
def get_data():
    room_id = request.args.get("room_id", "OverAll")
    room_list = json.loads(mongo_room_list())
    rooms = [item['room_id'] for item in room_list]
    try:
        if room_id == 'OverAll':
            room_list = json.loads(mongo_room_list())
            result = [{"room_id": item["room_id"], "status": item["status"]} for item in room_list]
            return render_template('list_room.html', liff_id=liff_id, rooms=rooms, result=result)
        else :
            room = json.loads(mongo_room_by_id(room_id))
            result = [{"room_id": item["room_id"], "status": item["status"]} for item in room]
            return render_template('list_room.html', liff_id=liff_id, rooms=rooms, result=result)
    except Exception as err :
        result = [{"status":"ERROR"}]
        return render_template('list_room.html', liff_id=liff_id, rooms=rooms, result=result)
