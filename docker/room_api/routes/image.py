# from flask import Blueprint, request, jsonify, send_from_directory
# import os
# import uuid
# import time
# # from utils.mongodb import mongo_img_insert

# # Initialize the blueprint for image handling
# image_blueprint = Blueprint('image', __name__)

# # Directory to store uploaded images
# IMAGE_DIR = "./images/"
# os.makedirs(IMAGE_DIR, exist_ok=True)


# # Upload image route
# @image_blueprint.route("/upload_image", methods=["POST"])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#     try:
#         file_uuid = str(uuid.uuid4())
#         filename = f"{file_uuid}.jpg"
#         image_path = os.path.join(IMAGE_DIR, filename)
#         file.save(image_path)
        
#         # Save timestamp and file UUID to MongoDB
#         timestamp = time.time()
#         local_time = time.localtime(timestamp)
#         readable_time = time.strftime("%d/%m/%y-%H:%M", local_time)
#         # mongo_img_insert(readable_time, file_uuid)

#         return jsonify({"message": "Image uploaded successfully", "file_uuid": file_uuid, "timestamp": readable_time}), 200
#     except Exception as e:
#         return jsonify({"error": f"Error processing image: {e}"}), 500

# # View image route
# @image_blueprint.route("/<uuid>", methods=["GET"])
# def show_image(uuid):
#     image_path = os.path.join(IMAGE_DIR, f"{uuid}.jpg")
    
#     if os.path.exists(image_path):
#         return send_from_directory(IMAGE_DIR, f"{uuid}.jpg", mimetype='image/jpeg')
#     else:
#         return jsonify({"error": "Image not found"}), 404