### app/config.py (Configuration settings)
import os


class Config:
    APP_URL = os.getenv("APP_URL", "http://localhost:5000")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
