from flask_restful import Resource, reqparse
from app.models.item import Item
from app.dto.item import ItemDTO
from app.database import db


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name cannot be blank"
    )

    def get(self, item_id):
        item = db.session.query(Item).get(item_id)
        if item:
            return ItemDTO.from_model(item), 200
        return {"message": "Item not found"}, 404

    def post(self):
        data = ItemResource.parser.parse_args()
        new_item = Item(name=data["name"])
        db.session.add(new_item)
        db.session.commit()
        return ItemDTO.from_model(new_item), 201
