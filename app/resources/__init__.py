from app.resources.item import ItemResource
from app.resources.user import UserResource


def initialize_routes(api):
    api.add_resource(ItemResource, "/item", "/item/<uuid:id>")
    api.add_resource(UserResource, "/user", "/user/<str:name>")
