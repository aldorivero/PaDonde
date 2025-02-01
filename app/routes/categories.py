from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.models.category import Category
from app.config import mongo

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')

@category_bp.route("/", methods=["POST"])
def create_category():
    data = request.json
    category = Category(
        name=data["name"],
        subcategories=data.get("subcategories", [])
    )
    category_id = category.save(mongo.db.categories)
    return jsonify({"id": str(category_id)}), 201

@category_bp.route("/", methods=["GET"])
def get_categories():
    categories = list(mongo.db.categories.find())
    for category in categories:
        category["_id"] = str(category["_id"])
    return jsonify(categories), 200

@category_bp.route("/<category_id>", methods=["GET"])
def get_category(category_id):
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    if not category:
        return jsonify({"error": "Category not found"}), 404
    category["_id"] = str(category["_id"])
    return jsonify(category), 200

@category_bp.route("/<category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.json
    updated_count = Category.update(mongo.db.categories, category_id, data)
    if updated_count == 0:
        return jsonify({"error": "Category not found or no changes made"}), 404
    return jsonify({"message": "Category updated successfully"}), 200

@category_bp.route("/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    deleted_count = Category.delete(mongo.db.categories, category_id)
    if deleted_count == 0:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"message": "Category deleted successfully"}), 200
