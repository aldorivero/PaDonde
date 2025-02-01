from bson import ObjectId
from pymongo.collection import Collection
from datetime import datetime

class Comment:
    def __init__(self, business_id: ObjectId, username: str, content: str, date=None):
        self.business_id = business_id
        self.username = username
        self.content = content
        self.date = date or datetime.utcnow()

    def save(self, collection: Collection):
        """Guardar el comentario en la base de datos"""
        comment_data = self.__dict__
        result = collection.insert_one(comment_data)
        return result.inserted_id
