from flask import Blueprint, request, jsonify
from app.config import mongo
from app.models.reservation import Reservation
from bson.objectid import ObjectId
from app.services.whatsapp_service import send_reservation_to_whatsapp

reservation_bp = Blueprint("reservations", __name__, url_prefix="/api/reservations")

@reservation_bp.route("/", methods=["GET"])
def get_reservations():
    """Obtiene todas las reservas o por negocio."""
    business_id = request.args.get("business_id")
    attended = request.args.get("attended")

    query = {}
    if business_id:
        query["business_id"] = business_id
    if attended is not None:
        query["attended"] = attended.lower() == "true"

    reservations = list(mongo.db.reservations.find(query))
    for reservation in reservations:
        reservation["_id"] = str(reservation["_id"])
    return jsonify(reservations), 200


@reservation_bp.route("/", methods=["POST"])
def create_reservation():
    """Crea una nueva reserva."""
    data = request.json
    reservation = Reservation(**data)
    result = mongo.db.reservations.insert_one(reservation.dict(by_alias=True))
    
     # Enviar la reserva al bot de WhatsApp
    send_reservation_to_whatsapp(reservation.dict(), data["customer_contact"])

    return jsonify({"message": "Reserva creada y enviada a WhatsApp", "id": str(result.inserted_id)}), 201


@reservation_bp.route("/<reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    """Actualiza una reserva."""
    data = request.json
    update_data = {key: value for key, value in data.items() if key != "id"}
    mongo.db.reservations.update_one(
        {"_id": ObjectId(reservation_id)}, {"$set": update_data}
    )
    return jsonify({"message": "Reserva actualizada"}), 200


@reservation_bp.route("/<reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    """Elimina una reserva."""
    mongo.db.reservations.delete_one({"_id": ObjectId(reservation_id)})
    return jsonify({"message": "Reserva eliminada"}), 200
