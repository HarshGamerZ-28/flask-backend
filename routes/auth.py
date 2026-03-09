from flask import Blueprint, jsonify, request
from extensions import db, bcrypt
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered!"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # create a token with user id inside
        token = create_access_token(identity=str(user.id))
        return jsonify({"message": "Login successful!", "token": token})
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

# protected route — only logged in users can access
@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

@auth.route("/users", methods=["POST"])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    return jsonify(result)# UPDATE user — requires login
@auth.route("/user/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found!"}), 404

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)

    db.session.commit()
    return jsonify({"message": "User updated successfully!"})


# DELETE user — requires login
@auth.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found!"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"})