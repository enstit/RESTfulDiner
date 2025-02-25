from flask_sqlalchemy import SQLAlchemy
from app.models import metadata

# Initialize extensions
db = SQLAlchemy(metadata=metadata)
