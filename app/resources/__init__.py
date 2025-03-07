# app/resources/__init__.py

from app.resources.department import DepartmentResource
from app.resources.printer import PrinterResource
from app.resources.user import LoginResource


def initialize_routes(api):
    # Authentication routes
    api.add_resource(LoginResource, "/login")

    api.add_resource(
        DepartmentResource,
        "/departments",
        "/departments/<string:_id>",
        "/departments/name=<string:name>",
    )
    api.add_resource(
        PrinterResource,
        "/printers",
        "/printers/<string:_id>",
        "/printers/name=<string:name>",
    )
