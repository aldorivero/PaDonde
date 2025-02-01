from twilio.rest import Client
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_reservation_to_whatsapp(reservation_data, whatsapp_to):
    """
    Envía los detalles de la reserva al bot de WhatsApp.
    :param reservation_data: Diccionario con los datos de la reserva.
    :param whatsapp_to: Número de WhatsApp del cliente o bot.
    """
    message_body = (
        f"¡Nueva Reserva!\n"
        f"Negocio: {reservation_data['business_name']}\n"
        f"Cliente: {reservation_data['customer_name']}\n"
        f"Contacto: {reservation_data['customer_phone']}\n"
        f"Fecha: {reservation_data['date']}\n"
        f"Hora: {reservation_data['time']}\n"
        f"Detalles: {reservation_data.get('details', 'N/A')}"
    )

    message = client.messages.create(
        body=message_body,
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{whatsapp_to}"
    )

    return message.sid
