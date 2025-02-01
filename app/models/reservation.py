from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

class Reservation(BaseModel):
    id: Optional[str] = Field(alias="_id")
    business_id: str
    customer_name: str
    customer_contact: str
    date: str  # Formato: YYYY-MM-DD
    time: str  # Formato: HH:MM
    status: str = "Pendiente"  # Por defecto, estado inicial
    attended: bool = False  # Por defecto, el cliente no ha acudido

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
