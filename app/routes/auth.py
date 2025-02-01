from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.config import mongo
from bson import ObjectId
from app.models.user import User
from app.models.role import Role

auth_bp = Blueprint("auth", __name__)

# Ejemplo: Registrar usuarios
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    # Extraer los datos de entrada
    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # Validar que todos los campos necesarios estén presentes
    if not all([name, email, username, password]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # Verificar si el email ya existe en la base de datos
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "El correo electrónico ya está registrado"}), 400

    # Verificar si el username ya existe en la base de datos
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "El nombre de usuario ya está registrado"}), 400

    # Crear una nueva instancia del usuario
    try:
        user = User(name=name, email=email, username=username, role_id=None, password=password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Insertar el usuario en la base de datos
    mongo.db.users.insert_one(user.to_dict())

    return jsonify({"message": "Usuario registrado exitosamente"}), 201


# Ejemplo: Login usuario
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get("identifier")  # 'identifier' puede ser 'email' o 'username'
    password = data.get("password")

    # Buscar el usuario por email o username
    user_data = mongo.db.users.find_one({"$or": [{"email": identifier}, {"username": identifier}]})
    if not user_data:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    user = User.from_dict(user_data)

    # Verificar la contraseña
    if not user.check_password(password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Crear el token JWT
    token = create_access_token(identity={"user_id": user.id, "role_id": user.role_id})
    return jsonify({"token": token}), 200
