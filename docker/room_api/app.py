import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# from routes.image import image_blueprint
from routes.room import room_blueprint

# app.register_blueprint(image_blueprint, url_prefix='/image')
app.register_blueprint(room_blueprint, url_prefix='/room')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')