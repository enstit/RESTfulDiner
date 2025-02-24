from flask_restful import Resource, reqparse
from app.models import Item, db


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name cannot be blank"
    )

    def get(self, item_id):
        item = Item.query.get(item_id)
        if item:
            return {"id": item.id, "name": item.name}, 200
        return {"message": "Item not found"}, 404

    def post(self):
        data = ItemResource.parser.parse_args()
        new_item = Item(name=data["name"])
        db.session.add(new_item)
        db.session.commit()
        return {"id": new_item.id, "name": new_item.name}, 201
