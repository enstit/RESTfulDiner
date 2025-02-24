from app.resources.item import ItemResource


def initialize_routes(api):
    print("🔥 Registering API routes...")  # Debugging output
    api.add_resource(ItemResource, "/item", "/item/<int:item_id>")
