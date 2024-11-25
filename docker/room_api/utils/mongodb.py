import os
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import logging
from bson import ObjectId

load_dotenv()

host = os.environ["MONGO_HOST"]
user = os.environ["MONGO_INITDB_ROOT_USERNAME"]
passwd = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
port = 27017

def mongo_room_by_id(id):
    mongoClient = MongoClient(f"mongodb://{user}:{passwd}@{host}:{port}")
    doc = mongoClient.db.rooms.find_one({"id": id})
    return doc
        
    
def mongo_room_list():
    mongoClient = MongoClient(f"mongodb://{user}:{passwd}@{host}:{port}")
    doc = mongoClient.db.rooms.find()
    return doc