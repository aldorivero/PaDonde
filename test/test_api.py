import unittest
from app.config import app, mongo  # Importa la instancia de Flask y MongoDB


class BusinessTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Configuración inicial del test """
        cls.client = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """ Limpiar después de ejecutar los tests """
        cls.app_context.pop()

    def test_create_business(self):
        """ Probar la creación de un negocio """
        response = self.client.post("/api/business/", json={
            "name": "Café Central",
            "address": "myLoacation",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "comments": [],
            "ratings": [],
            "categories": "Cafetería"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_nearby_businesses(self):
        """ Probar la búsqueda de negocios cercanos """
        response = self.client.get("/api/business/nearby?lat=19.4326&lon=-99.1332&category=cafe&max_distance=5000")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)  # Debe devolver una lista


if __name__ == "__main__":
    unittest.main()
