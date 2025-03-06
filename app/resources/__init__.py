# app/resources/__init__.py

from app.resources.department import DepartmentResource
from app.resources.item import ItemResource
from app.resources.printer import PrinterResource
from app.resources.user import LoginResource
from app.resources.user import UserResource


def initialize_routes(api):
    api.add_resource(
        DepartmentResource,
        "/departments",
        "/departments/<string:_id>",
        "/departments/name=<string:name>",
    )
    api.add_resource(
        ItemResource,
        "/items",
        "/items/<string:_id>",
        "/items/name=<string:name>",
    )
    api.add_resource(
        PrinterResource,
        "/printers",
        "/printers/<string:_id>",
        "/printers/name=<string:name>",
    )

    # Authentication routes
    api.add_resource(UserResource, "/users")
    api.add_resource(LoginResource, "/login")
