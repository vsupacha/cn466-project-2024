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
    """Get list of unique rooms based on the room_id field."""
    db = mongo_connect()
    try:
        # Aggregate rooms to find unique entries by room_id
        rooms = list(
            db.rooms.aggregate([
                {"$group": {
                    "_id": "$room_id",  # Group by the room_id field
                    "latest_entry": {"$first": "$$ROOT"}  # Take the first document for each group
                }},
                {"$replaceRoot": {"newRoot": "$latest_entry"}}  # Replace the root with the grouped document
            ])
        )
        return dumps(rooms)  # Converts the BSON documents to JSON
    except Exception as e:
        logging.error(f"Error fetching unique room list by room_id: {e}")
        return None
