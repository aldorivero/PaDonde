import bcrypt
from bson import ObjectId
import re

class User:
    def __init__(self, name, email, username, role_id, password, _id=None):
        self.id = str(_id) if _id else None
        self.name = name
        self.email = email
        self.username = username
        self.password = self.hash_password(password)
        self.role_id = str(role_id) if role_id else None

        # Validaciones
        self.validate_email()
        self.validate_username()
        self.validate_password()

    def validate_email(self):
        """Validar que el correo tenga el formato correcto"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("El correo electrónico no tiene un formato válido")

    def validate_username(self):
        """Validar que el nombre de usuario no esté vacío"""
        if not self.username or len(self.username.strip()) == 0:
            raise ValueError("El nombre de usuario no puede estar vacío")

    def validate_password(self):
        """Validar que la contraseña tenga al menos 8 caracteres"""
        if len(self.password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

    def hash_password(self, password):
        """Generar un hash para la contraseña"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Comprobar si la contraseña proporcionada es correcta"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        data = {
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "role_id": ObjectId(self.role_id) if self.role_id else None,
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name"),
            email=data.get("email"),
            username=data.get("username"),
            role_id=data.get("role_id"),
            password=data.get("password"),
            _id=data.get("_id"),
        )
