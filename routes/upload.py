from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os

upload = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided!"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected!"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed!"}), 400

    filename = secure_filename(file.filename)  # ✅ inside function
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

    return jsonify({"message": "File uploaded successfully!", "filename": filename}), 201