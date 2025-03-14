# app/resources/__init__.py

from app.resources.delivery_station import DeliveryStationResource
from app.resources.department import DepartmentResource
from app.resources.item import ItemResource
from app.resources.printer import PrinterResource
from app.resources.user import LoginResource
from app.resources.order import OrderResource


def initialize_routes(api):
    # Authentication routes
    api.add_resource(LoginResource, "/login")

    api.add_resource(
        DeliveryStationResource,
        "/delivery_stations",
        "/delivery_stations/<string:_id>",
        "/delivery_stations/name=<string:name>",
    )
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
    api.add_resource(OrderResource, "/orders", "/orders/<string:_id>")
    api.add_resource(
        PrinterResource,
        "/printers",
        "/printers/<string:_id>",
        "/printers/name=<string:name>",
    )
