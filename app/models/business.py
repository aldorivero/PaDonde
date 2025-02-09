from bson import ObjectId
from app.config import mongo
from pymongo.collection import Collection

class Business:
    def __init__(self, name: str, address: str, latitude: float, longitude: float, comments=None, ratings=None, categories=None):
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.comments = comments or []  # Lista de IDs de comentarios
        self.ratings = ratings or []    # Lista de IDs de puntuaciones
        self.categories = categories or []  # Lista de IDs de categorías

    def save(self, collection: Collection):
        """Guardar el negocio en la base de datos"""
        business_data = self.__dict__
        result = collection.insert_one(business_data)
        return result.inserted_id
    
    @staticmethod
    def update(collection: Collection, business_id: str, update_data: dict):
        """Actualizar un negocio"""
        result = collection.update_one(
            {"_id": ObjectId(business_id)},
            {"$set": update_data}
        )
        return result.modified_count

    @staticmethod
    def delete(collection: Collection, business_id: str):
        """Eliminar un negocio"""
        result = collection.delete_one({"_id": ObjectId(business_id)})
        return result.deleted_count


    @staticmethod
    def get_nearby_businesses(lat, lon, category, max_distance=5000):
        return mongo.db.businesses.find({
            "categories": {"$in": [category]},
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "$maxDistance": max_distance
                }
            }
        })
