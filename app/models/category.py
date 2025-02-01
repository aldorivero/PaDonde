from bson import ObjectId
from pymongo.collection import Collection

class Category:
    def __init__(self, name: str, parent_id: ObjectId = None):
        self.name = name
        self.parent_id = parent_id  # ID de la categoría padre

    def save(self, collection: Collection):
        """Guardar la categoría en la base de datos"""
        category_data = self.__dict__
        result = collection.insert_one(category_data)
        return result.inserted_id
    
    @staticmethod
    def update(collection: Collection, category_id: str, update_data: dict):
        """Actualizar una categoría"""
        result = collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": update_data}
        )
        return result.modified_count

    @staticmethod
    def delete(collection: Collection, category_id: str):
        """Eliminar una categoría"""
        result = collection.delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count
