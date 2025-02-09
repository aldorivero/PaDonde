import unittest
from app.config import app, mongo
from bson import ObjectId

class BusinessTestCase(unittest.TestCase):
    def setUp(self):
        """Configurar el entorno de prueba"""
        self.client = app.test_client()
        self.db = mongo.db
        self.businesses = self.db.businesses  # Colección de negocios

        # Datos de prueba
        self.test_business = {
            "name": "Café Central",
            "address": "myLocation",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "comments": [],
            "ratings": [],
            "categories": ["Cafetería"],
            "location": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128]
            }
        }

    def tearDown(self):
        """Limpiar la base de datos después de cada prueba"""
        self.businesses.delete_many({})

    def test_create_business(self):
        """Probar la creación de un negocio"""
        response = self.client.post("/api/business/", json=self.test_business)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_update_business(self):
        """Probar la actualización de un negocio"""
        inserted_id = self.businesses.insert_one(self.test_business).inserted_id
        update_data = {"name": "Nuevo Nombre"}

        response = self.client.put(f"/api/business/{inserted_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_business = self.businesses.find_one({"_id": ObjectId(inserted_id)})
        self.assertEqual(updated_business["name"], "Nuevo Nombre")

    def test_delete_business(self):
        """Probar la eliminación de un negocio"""
        inserted_id = self.businesses.insert_one(self.test_business).inserted_id
        response = self.client.delete(f"/api/business/{inserted_id}")
        self.assertEqual(response.status_code, 200)
        deleted_business = self.businesses.find_one({"_id": ObjectId(inserted_id)})
        self.assertIsNone(deleted_business)

    def test_get_nearby_businesses(self):
        """Probar la obtención de negocios cercanos"""
        self.businesses.insert_one(self.test_business)

        response = self.client.get("/api/business/nearby?lat=40.7128&lon=-74.0060&category=Cafetería&max_distance=5000")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)

if __name__ == "__main__":
    unittest.main()
