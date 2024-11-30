import os
from dotenv import load_dotenv
from utils.mongodb import mongo_room_list, mongo_room_by_id
load_dotenv()

from flask import request, abort, Blueprint, template_rendered
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

# Load environment variables
load_dotenv()

line_blueprint = Blueprint('line', __name__)

configuration = Configuration(access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

@line_blueprint.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text
    reply_text = create_reply(user_message)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )

def create_reply(user_message):
    if user_message == "#list":
        rooms_json = mongo_room_list()  # Get all unique rooms

        if rooms_json:  # Ensure rooms are returned as a JSON string
            rooms = json.loads(rooms_json)  # Parse JSON string into a Python object (list of dictionaries)
            
            # Create a list of rooms to display
            reply_text = "Here are the rooms:\n"
            for room in rooms:
                if isinstance(room, dict) and 'room_id' in room and 'status' in room:
                    status = map_status(room['status'])  # Map the status to a user-friendly message
                    reply_text += f"Room {room['room_id']} - {status}\n"
                else:
                    reply_text += "Error with room data.\n"
        else:
            reply_text = "Sorry, I couldn't find any rooms."
    
    elif user_message.startswith("#room_id"):  # Corrected to `startswith`
        room_id = user_message.split()[1]  # Extract room_id from the message
        room_json = mongo_room_by_id(room_id)  # Fetch room by room_id
        
        if room_json:  # Ensure room is found before using it
            room = json.loads(room_json)  # Parse JSON string into a Python object (list or dictionary)
            
            # Check if room is a list (MongoDB query result might return a list)
            if isinstance(room, list) and len(room) > 0:
                room = room[0]  # Get the first item in the list (which should be the room dictionary)
            
            # Now we can safely access room['status'] if it's a dictionary
            if isinstance(room, dict) and 'room_id' in room and 'status' in room:
                status = map_status(room['status'])  # Map the status to a user-friendly message
                reply_text = f"Room {room['room_id']} - {status}\n"
            else:
                reply_text = "Error with room data.\n"
        else:
            reply_text = f"Sorry, I couldn't find room {room_id}."

    else:
        reply_text = f"You said: {user_message}"

    return reply_text

def map_status(status):
    """Converts numeric status to a human-readable string."""
    if status == 0:
        return "Available"
    elif status == 1:
        return "Occupied"
    else:
        return "Unknown Status"