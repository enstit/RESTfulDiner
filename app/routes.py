from app.resources.item import ItemResource
from app.resources.user import UserResource


def initialize_routes(api):
    print("🔥 Registering API routes...")  # Debugging output
    api.add_resource(ItemResource, "/item", "/item/<uuid:id>")
    api.add_resource(UserResource, "/user", "/user/<string:name>")
