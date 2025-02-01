from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.config import mongo
from bson import ObjectId
from app.models.role import Role

roles_bp = Blueprint("roles", __name__)

@roles_bp.route("/", methods=["POST"])
def create_role():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    permissions = data.get("permissions", [])

    if not all([name, description]):
        return jsonify({"error": "El nombre y la descripción son obligatorios"}), 400

    # Crear rol
    role = Role(name=name, description=description, permissions=permissions)

    # Insertar en la base de datos
    mongo.db.roles.insert_one(role.to_dict())

    return jsonify({"message": "Rol creado exitosamente"}), 201

@roles_bp.route("/", methods=["GET"])
def get_roles():
    roles_data = mongo.db.roles.find()
    roles = [Role.from_dict(role) for role in roles_data]

    return jsonify([role.to_dict() for role in roles]), 200

@roles_bp.route("/<role_id>", methods=["GET"])
def get_role(role_id):
    role_data = mongo.db.roles.find_one({"_id": ObjectId(role_id)})
    if not role_data:
        return jsonify({"error": "Rol no encontrado"}), 404

    role = Role.from_dict(role_data)
    return jsonify(role.to_dict()), 200

@roles_bp.route("/<role_id>", methods=["PUT"])
def update_role(role_id):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    permissions = data.get("permissions", [])

    role_data = mongo.db.roles.find_one({"_id": ObjectId(role_id)})
    if not role_data:
        return jsonify({"error": "Rol no encontrado"}), 404

    role = Role.from_dict(role_data)

    # Actualizar rol
    if name:
        role.name = name
    if description:
        role.description = description
    if permissions:
        role.permissions = permissions

    # Actualizar en la base de datos
    mongo.db.roles.update_one({"_id": ObjectId(role_id)}, {"$set": role.to_dict()})

    return jsonify({"message": "Rol actualizado exitosamente"}), 200

@roles_bp.route("/<role_id>", methods=["DELETE"])
def delete_role(role_id):
    role_data = mongo.db.roles.find_one({"_id": ObjectId(role_id)})
    if not role_data:
        return jsonify({"error": "Rol no encontrado"}), 404

    mongo.db.roles.delete_one({"_id": ObjectId(role_id)})
    return jsonify({"message": "Rol eliminado exitosamente"}), 200
