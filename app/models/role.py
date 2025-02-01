from bson import ObjectId

class Role:
    def __init__(self, name, description, permissions=None, _id=None):
        self.id = str(_id) if _id else None
        self.name = name
        self.description = description
        self.permissions = permissions or []  # Lista de permisos como strings

        # Validaciones
        self.validate_name()

    def validate_name(self):
        """Validar que el nombre del rol no esté vacío"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("El nombre del rol no puede estar vacío")

    def to_dict(self):
        data = {
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

    @staticmethod
    def from_dict(data):
        return Role(
            name=data.get("name"),
            description=data.get("description"),
            permissions=data.get("permissions", []),
            _id=data.get("_id"),
        )
