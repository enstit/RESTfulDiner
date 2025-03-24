### app/extensions.py

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.models import metadata

# Initialize extensions
jwt = JWTManager()
db = SQLAlchemy(metadata=metadata)
