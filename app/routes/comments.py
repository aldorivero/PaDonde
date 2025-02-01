from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.models.comment import Comment
from app.config import mongo

comment_bp = Blueprint('comment', __name__, url_prefix='/api/comments')

@comment_bp.route("/", methods=["POST"])
def create_comment():
    data = request.json
    comment = Comment(
        business_id=ObjectId(data["business_id"]),
        username=data["username"],
        content=data["content"]
    )
    comment_id = comment.save(mongo.db.comments)
    return jsonify({"id": str(comment_id)}), 201

@comment_bp.route("/<business_id>", methods=["GET"])
def get_comments(business_id):
    comments = list(mongo.db.comments.find({"business_id": ObjectId(business_id)}))
    for comment in comments:
        comment["_id"] = str(comment["_id"])
    return jsonify(comments), 200

