from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.models.business import Business
from app.config import mongo

business_bp = Blueprint('business', __name__, url_prefix='/api/businesses')

@business_bp.route("/", methods=["POST"])
def create_business():
    data = request.json
    business = Business(
        name=data["name"],
        address=data["address"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        comments=[],
        ratings=[],
        categories=data["categories"]
    )
    business_id = business.save(mongo.db.businesses)
    return jsonify({"id": str(business_id)}), 201

@business_bp.route("/", methods=["GET"])
def get_businesses():
    businesses = list(mongo.db.businesses.find())
    for business in businesses:
        business["_id"] = str(business["_id"])
    return jsonify(businesses), 200

@business_bp.route("/<business_id>", methods=["GET"])
def get_business(business_id):
    business = mongo.db.businesses.find_one({"_id": ObjectId(business_id)})
    if not business:
        return jsonify({"error": "Business not found"}), 404
    business["_id"] = str(business["_id"])
    return jsonify(business), 200

@business_bp.route("/<business_id>", methods=["PUT"])
def update_business(business_id):
    data = request.json
    updated_count = Business.update(mongo.db.businesses, business_id, data)
    if updated_count == 0:
        return jsonify({"error": "Business not found or no changes made"}), 404
    return jsonify({"message": "Business updated successfully"}), 200

@business_bp.route("/<business_id>", methods=["DELETE"])
def delete_business(business_id):
    deleted_count = Business.delete(mongo.db.businesses, business_id)
    if deleted_count == 0:
        return jsonify({"error": "Business not found"}), 404
    return jsonify({"message": "Business deleted successfully"}), 200

@business_bp.route("/nearby", methods=["GET"])
def get_nearby_businesses():
    lat = float(request.args.get("lat", 0))
    lon = float(request.args.get("lon", 0))
    category = request.args.get("category", "")
    max_distance = int(request.args.get("max_distance", 5000))

    businesses = Business.get_nearby_businesses(lat, lon, category, max_distance)

    results = []
    for business in businesses:
        business["_id"] = str(business["_id"])
        results.append(business)

    return jsonify(results), 200

