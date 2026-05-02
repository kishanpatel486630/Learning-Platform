import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Admin backend configuration."""
    SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "admin-dev-secret-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    
    # Use the same database as the User Site
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/learnpath")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "learnpath")
    
    # JWT for Admin
    JWT_SECRET = os.getenv("ADMIN_JWT_SECRET", "admin-jwt-secret-change-me")
    JWT_ACCESS_EXPIRY = timedelta(hours=24)
    
    # Admin CORS (Port 5001 or standard frontend ports)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5001,http://127.0.0.1:5001,http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000").split(",")

config = Config()
