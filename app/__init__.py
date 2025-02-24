from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.config import Config

# Initialize extensions
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize plugins
    db.init_app(app)

    api = Api(
        app, prefix="/api/v1", catch_all_404s=True, serve_challenge_on_401=True
    )
    # api.init_app(app)

    # Manually register the resource
    from app.resources.item import ItemResource

    api.add_resource(ItemResource, "/item", "/item/<int:item_id>")

    with app.app_context():
        db.create_all()

    return app
