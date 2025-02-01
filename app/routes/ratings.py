from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.models.rating import Rating
from app.config import mongo

rating_bp = Blueprint('rating', __name__, url_prefix='/api/ratings')

@rating_bp.route("/", methods=["POST"])
def create_rating():
    data = request.json
    if not (1 <= data["score"] <= 5):
        return jsonify({"error": "Score must be between 1 and 5"}), 400
    
    rating = Rating(
        business_id=ObjectId(data["business_id"]),
        username=data["username"],
        score=data["score"]
    )
    rating_id = rating.save(mongo.db.ratings)
    return jsonify({"id": str(rating_id)}), 201

@rating_bp.route("/<business_id>", methods=["GET"])
def get_ratings(business_id):
    ratings = list(mongo.db.ratings.find({"business_id": ObjectId(business_id)}))
    for rating in ratings:
        rating["_id"] = str(rating["_id"])
    return jsonify(ratings), 200
