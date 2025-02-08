from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/padonde")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_token")

# Configuración de Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "default_account_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "default_auth_token")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos MongoDB
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)  # Inicializar PyMongo

# Configuración de JWT
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY # Cambia esto por una clave secreta segura
jwt = JWTManager(app)  # Inicializa el JWTManager con la app

# Registrar Blueprints
from app.routes.auth import auth_bp
from app.routes.roles import roles_bp
from app.routes.users import users_bp
from app.routes.comments import comment_bp
from app.routes.ratings import rating_bp
from app.routes.business import business_bp
from app.routes.categories import category_bp
from app.routes.reservations import reservation_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(roles_bp, url_prefix="/api/roles")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(comment_bp, url_prefix="/api/comments")
app.register_blueprint(rating_bp, url_prefix="/api/ratings")
app.register_blueprint(business_bp, url_prefix="/api/business")
app.register_blueprint(category_bp, url_prefix="/api/categories")
app.register_blueprint(reservation_bp, url_prefix="/api/reservations")

# Ruta por defecto
@app.route('/')
def home():
    return "Bienvenido a la API PaDonde"