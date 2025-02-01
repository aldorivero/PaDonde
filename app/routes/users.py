from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.config import mongo
from bson import ObjectId
from app.models.role import Role
from app.models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role_id = data.get("role_id")

    if not all([name, email, username, password]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # Verificar si el email o el username ya existen
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "El correo electrónico ya está registrado"}), 400
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "El nombre de usuario ya está registrado"}), 400

    # Crear el usuario
    try:
        user = User(name=name, email=email, username=username, role_id=role_id, password=password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Insertar en la base de datos
    mongo.db.users.insert_one(user.to_dict())

    return jsonify({"message": "Usuario creado exitosamente"}), 201

@users_bp.route("/", methods=["GET"])
def get_users():
    users_data = mongo.db.users.find()
    users = [User.from_dict(user) for user in users_data]

    return jsonify([user.to_dict() for user in users]), 200


@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return jsonify({"error": "Usuario no encontrado"}), 404

    user = User.from_dict(user_data)
    return jsonify(user.to_dict()), 200


@users_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role_id = data.get("role_id")

    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return jsonify({"error": "Usuario no encontrado"}), 404

    user = User.from_dict(user_data)

    # Actualizar campos
    if name:
        user.name = name
    if email:
        user.email = email
    if username:
        user.username = username
    if password:
        user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    if role_id:
        user.role_id = role_id

    # Actualizar en la base de datos
    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user.to_dict()})

    return jsonify({"message": "Usuario actualizado exitosamente"}), 200


@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return jsonify({"error": "Usuario no encontrado"}), 404

    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

