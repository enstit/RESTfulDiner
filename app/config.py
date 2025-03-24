### app/config.py

import os


class Config:
    APP_URL = os.getenv("APP_URL", "http://localhost:5000")
    API_URI = os.getenv("API_URI", "/api/v1")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
    UUID_SECRET1 = os.getenv("UUID_SECRET1", "secret1")
    UUID_SECRET2 = os.getenv("UUID_SECRET2", "secret2")
