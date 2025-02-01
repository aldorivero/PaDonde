from bson import ObjectId
from pymongo.collection import Collection

class Rating:
    def __init__(self, business_id: ObjectId, username: str, score: int):
        self.business_id = business_id
        self.username = username
        self.score = score

    def save(self, collection: Collection):
        """Guardar la puntuación en la base de datos"""
        rating_data = self.__dict__
        result = collection.insert_one(rating_data)
        return result.inserted_id
