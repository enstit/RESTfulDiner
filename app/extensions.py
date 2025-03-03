from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.models import metadata

# Initialize extensions
jwt = JWTManager()
db = SQLAlchemy(metadata=metadata)
