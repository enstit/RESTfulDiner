### app/config.py (Configuration settings)
import os


class Config:
    APP_URL = "https://diner.enricostefanel.it"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        # "sqlite:///:memory:",
        "postgresql://sagrevolution:sagrevolution@srv-ud01:5432/postgres",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "token")
