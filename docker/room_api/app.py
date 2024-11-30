import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# from routes.image import image_blueprint
from routes.room import room_blueprint
from routes.line import line_blueprint
from routes.liff import liff_blueprint

# app.register_blueprint(image_blueprint, url_prefix='/image')
app.register_blueprint(room_blueprint, url_prefix='/room')
app.register_blueprint(line_blueprint, url_prefix='/line')
app.register_blueprint(liff_blueprint, url_prefix='/liff')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')