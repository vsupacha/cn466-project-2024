import os
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
from bson import ObjectId
from bson.json_util import dumps

# Load environment variables
load_dotenv()

# Environment variable setup
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))  # Default port is 27017

# Utility functions
def mongo_connect():
    """Create a MongoClient connection."""
    try:
        client = MongoClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"
        )
        return client.db  # Return the specific database
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        raise

def mongo_room_by_id(room_id):
    """Get room by ID."""
    db = mongo_connect()
    try:
        room = db.rooms.find_one({"_id": ObjectId(room_id)})
        if room:
            return dumps(room)  # Converts the BSON document to JSON
        return None
    except Exception as e:
        logging.error(f"Error fetching room by ID: {e}")
        return None

def mongo_room_list():
    """Get list of all rooms."""
    db = mongo_connect()
    try:
        rooms = list(db.rooms.find())
        return dumps(rooms)  # Converts the BSON documents to JSON
    except Exception as e:
        logging.error(f"Error fetching room list: {e}")
        return None