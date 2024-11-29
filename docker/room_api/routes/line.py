import os
from dotenv import load_dotenv
from utils.mongodb import mongo_room_list, mongo_room_by_id
load_dotenv()

from flask import request, abort, Blueprint, template_rendered

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

@line_blueprint.route("/liff")
def liff():
    return template_rendered("index.html", liff_id=os.environ["LIFF_ID"])

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
        rooms = mongo_room_list()  # Get all unique rooms

        if rooms:  # Ensure rooms are returned as a list of dictionaries
            # Create a list of rooms to display
            reply_text = "Here are the rooms:\n"
            for room in rooms:
                # Assuming room is a dictionary, and it has keys 'room_id' and 'status'
                status = map_status(room['status'])  # Map the status to a user-friendly message
                reply_text += f"Room {room['room_id']} - {status}\n"
        else:
            reply_text = "Sorry, I couldn't find any rooms."
    
    elif user_message.startswith("#room_id"):  # Corrected to `startswith`
        room_id = user_message.split()[1]  # Extract room_id from the message
        room = mongo_room_by_id(room_id)  # Fetch room by room_id
        
        if room:  # Ensure room is found before using it
            # Assuming room is a dictionary and has the 'status' field
            status = map_status(room['status'])  # Convert status to user-friendly string
            reply_text = f"The status of Room {room['room_id']} is {status}."
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
