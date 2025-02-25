from flask import Flask
from flask_restful import Api
from app.config import Config
from app.database import db
from app.resources import initialize_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize plugins
    db.init_app(app)

    api = Api(
        app, prefix="/api/v1", catch_all_404s=True, serve_challenge_on_401=True
    )
    api.init_app(app)

    # Initialize routes
    initialize_routes(api)

    with app.app_context():
        db.create_all()

    return app
