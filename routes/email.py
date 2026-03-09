from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from extensions import mail
from flask_mail import Message

email_bp = Blueprint("email_bp", __name__)

@email_bp.route("/send-email", methods=["POST"])
@jwt_required()
def send_email():
    data = request.get_json()
    to = data["to"]
    subject = data["subject"]
    body = data["body"]

    msg = Message(
        subject=subject,
        sender="your_gmail@gmail.com",
        recipients=[to]
    )
    msg.body = body
    mail.send(msg)

    return jsonify({"message": "Email sent successfully!"}), 200