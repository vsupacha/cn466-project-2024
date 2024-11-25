import os
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import logging
from bson import ObjectId

load_dotenv()

# Environment variable setup
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)  # Default port is 27017
MONGO_DB = os.getenv("MONGO_DB_NAME", "db")  # Default DB name

# Utility functions
def mongo_connect():
    """Create a MongoClient connection."""
    return MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")

def mongo_room_by_id(room_id):
    """Get room by ID."""
    client = mongo_connect()
    try:
        room = client[MONGO_DB].rooms.find_one({"_id": ObjectId(room_id)})
        return room
    except Exception as e:
        logging.error(f"Error fetching room by ID: {e}")
        return None
    finally:
        client.close()

def mongo_room_list():
    """Get list of all rooms."""
    client = mongo_connect()
    try:
        rooms = list(client[MONGO_DB].rooms.find())
        return rooms
    except Exception as e:
        logging.error(f"Error fetching room list: {e}")
        return []
    finally:
        client.close()