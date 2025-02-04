from app import mongo

class Place:
    @staticmethod
    def create_place(name, category, latitude, longitude):
        place = {
            "name": name,
            "category": category,
            "location": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }
        }
        return mongo.db.places.insert_one(place)

    @staticmethod
    def get_nearby_places(lat, lon, category, max_distance=5000):
        return mongo.db.places.find({
            "category": category,
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
