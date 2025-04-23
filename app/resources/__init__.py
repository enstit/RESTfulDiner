# app/resources/__init__.py

from app.resources.delivery_station import DeliveryStationResource
from app.resources.department import DepartmentResource
from app.resources.event import EventResource
from app.resources.item import ItemResource
from app.resources.kiosk import KioskResource
from app.resources.order import OrderResource, DepartmentOrderResource
from app.resources.printer import PrinterResource
from app.resources.user import UserResource, LoginResource, LogoutResource


def initialize_routes(api):
    api.add_resource(EventResource, "/events", "/events/<string:event_id>")
    api.add_resource(UserResource, "/users", "/users/<string:user_id>")
    api.add_resource(LoginResource, "/users/<string:user_id>/login")
    api.add_resource(LogoutResource, "/users/<string:user_id>/logout")

    api.add_resource(
        DeliveryStationResource,
        "/delivery_stations",
        "/delivery_stations/<string:delivery_station_id>",
    )
    api.add_resource(
        DepartmentResource,
        "/departments",
        "/departments/<string:department_id>",
    )
    api.add_resource(
        KioskResource,
        "/kiosks",
        "/kiosks/<string:kiosk_id>",
    )
    api.add_resource(ItemResource, "/items", "/items/<string:item_id>")
    api.add_resource(OrderResource, "/orders", "/orders/<string:order_id>")
    api.add_resource(
        DepartmentOrderResource,
        "/departments/<string:department_id>/orders",
        "/departments/<string:department_id>/orders/<string:order_id>",
    )
    api.add_resource(PrinterResource, "/printers", "/printers/<string:_id>")
