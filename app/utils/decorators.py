from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify
from bson import ObjectId
from app.config import mongo

def role_required(permission):
    """
    Decorador para verificar si el rol del usuario tiene el permiso requerido.
    """
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            # Obtener la identidad del token JWT
            identity = get_jwt_identity()
            role_id = identity.get("role_id")

            # Buscar el rol en la base de datos
            role = mongo.db.roles.find_one({"_id": ObjectId(role_id)})
            if not role or permission not in role.get("permissions", []):
                return jsonify({"error": "No tienes permiso para realizar esta acción"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
