from flask import Flask
from flask_restful import Api

from app.config import Config
from app.extensions import db
from app.extensions import jwt
from app.models.printer import Printer
from app.models.user import User
from app.models.user import UserRoleType
from app.resources import initialize_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize plugins
    db.init_app(app)
    jwt.init_app(app)

    api = Api(app, prefix="/api/v1", catch_all_404s=True)
    api.init_app(app)

    # Initialize routes
    initialize_routes(api)

    with app.app_context():
        db.create_all()

        # Add sample data for README tutorial
        db.session.add(
            Printer(
                name="KitchenPrinter",
                mac_address="32:1c:35:93:4e:07",
                ip_address="10.172.54.145",
            )
        )
        db.session.add(
            User(username="admin", password="admin", role=UserRoleType.ADMIN)
        )
        db.session.add(
            User(username="test", password="test", role=UserRoleType.OPERATOR)
        )
        db.session.commit()

    return app
