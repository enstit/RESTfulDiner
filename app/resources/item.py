# app/resources/item.py

from flask_restful import Resource
from flask_restful import reqparse

from app.extensions import db
from app.dto.item import ItemDTO
from app.models.department import Department
from app.models.item import Item
from app.models.item import MenuSectionType
from app.models.item import OrderStatusType


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name of the food item"
    )
    parser.add_argument(
        "description",
        type=str,
        required=False,
        help="Description of the food item",
    )
    parser.add_argument(
        "department",
        type=str,
        required=True,
        help="Name of the department the food item belongs to",
    )
    parser.add_argument(
        "menu_section",
        type=str,
        required=True,
        choices=[section.name for section in MenuSectionType],
        help="Name of the menu section the food item belongs to",
    )
    parser.add_argument(
        "price", type=float, required=True, help="Price of the food item"
    )
    parser.add_argument(
        "deposit",
        type=float,
        required=False,
        help="Deposit of the food item, if any",
    )
    parser.add_argument(
        "availability",
        type=int,
        required=False,
        help="Initial number of available food items, if any",
    )
    parser.add_argument(
        "initial_status",
        type=str,
        required=True,
        choices=[status.name for status in OrderStatusType],
        default=OrderStatusType.COMPLETED.name,
        help="Initial status of the food item",
    )

    def get(self, *, id: str | None = None, name: str | None = None):
        if id or name:
            item = (
                db.session.query(Item)
                .where(Item.id == id if id else Item.name == name)
                .one_or_none()
            )
            if item:
                return ItemDTO.from_model(item), 200
            return {"message": f"Item {name} was not found"}, 404
        items = db.session.query(Item).all()
        return ItemDTO.from_model_list(items), 200

    def post(self):
        data = ItemResource.parser.parse_args()
        department = (
            db.session.query(Department)
            .where(Department.name == data["department"])
            .one_or_none()
        )
        new_item = Item(
            name=data["name"],
            description=data["description"],
            department=department,
            menu_section=MenuSectionType[data["menu_section"]],
            price=data["price"],
            deposit=data["deposit"],
            availability=data["availability"],
            initial_status=OrderStatusType[data["initial_status"]],
        )
        db.session.add(new_item)
        db.session.commit()
        return ItemDTO.from_model(new_item), 201
