from flask import Blueprint, request, jsonify
from app.models.place import Place

places_bp = Blueprint("places", __name__)

@places_bp.route("/add", methods=["POST"])
def add_place():
    data = request.json
    name = data.get("name")
    category = data.get("category")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not all([name, category, latitude, longitude]):
        return jsonify({"error": "Faltan datos"}), 400

    place_id = Place.create_place(name, category, latitude, longitude)
    return jsonify({"message": "Lugar agregado", "id": str(place_id.inserted_id)}), 201

@places_bp.route("/nearby", methods=["GET"])
def get_places():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    category = request.args.get("category")

    if not category:
        return jsonify({"error": "Se requiere una categoría"}), 400

    nearby_places = Place.get_nearby_places(lat, lon, category)
    result = [{"name": p["name"], "location": p["location"]["coordinates"]} for p in nearby_places]

    return jsonify(result), 200
