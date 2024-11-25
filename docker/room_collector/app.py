import paho.mqtt.client as mqttc
import time
import json
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

MQTT_BROKER ="mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_SUB_TOPIC = "TU/CN466/tsimcam/#"
MQTT_PUB_TOPIC = "TU/CN466/tsimcam"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(MQTT_SUB_TOPIC)
        else:
            print("Failed to connect, return code %d\n", rc)
        
    def on_message(client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode('utf-8'))
        print(topic, payload)
        print("Create new document")
        db = mongoClient.db
        tsimcam = db.rooms
        doc = {
            "timestamp" : payload["timestamp"],
            "status" : payload["status"]
            }
        tsimcam.insert_one(doc)
            
    client = mqttc.Client(mqttc.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

host = os.getenv("MONGO_HOST")
user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
passwd = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
port = 27017
mongoClient = MongoClient(host=host, port=port, username=user, password=passwd)
mqttClient = connect_mqtt()

while True:
    time.sleep(3)
    mqttClient.loop()

    