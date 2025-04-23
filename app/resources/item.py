# app/resources/item.py

from flask_restful import reqparse

from app.dto.item import ItemDTO
from app.extensions import db
from app.models._types import MenuSectionType, OrderStatusType
from app.models.cfg_department import CfgDepartment
from app.models.cfg_item import CfgItem
from app.resources.auth import ProtectedResource


class ItemResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("description", type=str)
    parser.add_argument("department_id", type=str)
    parser.add_argument("menu_section", type=str)
    parser.add_argument("price", type=float)
    parser.add_argument("deposit", type=float)
    parser.add_argument("availability", type=int)
    parser.add_argument("initial_status", type=str)

    def get(
        self, *, item_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if item_id:
            item = (
                db.session.query(CfgItem)
                .filter(
                    CfgItem.event_id == msg.get("event_id"),
                    CfgItem.item_id == item_id,
                )
                .one_or_none()
            )
            if item:
                return ItemDTO.from_model(item), 200
            return {
                "error": f"Item {item_id} was not found in the current event"
            }, 404
        items = (
            db.session.query(CfgItem)
            .filter(CfgItem.event_id == msg.get("event_id"))
            .all()
        )
        return ItemDTO.from_model_list(items), 200

    def post(self):
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = ItemResource.parser.parse_args()
        department = (
            db.session.query(CfgDepartment)
            .filter(
                CfgDepartment.event_id == msg.get("event_id"),
                CfgDepartment.department_id == data["department_id"],
            )
            .one_or_none()
        )
        new_item = CfgItem(
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
