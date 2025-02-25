from app.resources.department import DepartmentResource
from app.resources.item import ItemResource
from app.resources.user import UserResource
from app.resources.printer import PrinterResource


def initialize_routes(api):
    api.add_resource(
        DepartmentResource,
        "/department",
        "/department/<string:id>",
        "/department/name=<string:name>",
    )
    api.add_resource(
        ItemResource,
        "/item",
        "/item/<string:id>",
        "/item/name=<string:name>",
    )
    api.add_resource(
        UserResource,
        "/user",
        "/user/<string:id>",
        "/user/username=<string:username>",
    )
    api.add_resource(
        PrinterResource,
        "/printer",
        "/printer/<string:id>",
        "/printer/name=<string:name>",
    )
