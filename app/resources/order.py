# app/resources/item.py

from cerberus import Validator
import json

from flask_restful import reqparse

from app.extensions import db
from app.dto.order import OrderDTO
from app.models.department_order import DepartmentOrder
from app.models.department_order_item import DepartmentOrderItem
from app.models.order import Order
from app.models.item import Item
from app.models.order import PaymentMethodType
from app.resources.auth import ProtectedResource


class OrderResource(ProtectedResource):

    @staticmethod
    def order_validator(value):
        v = Validator(
            {
                "item_id": {"required": True, "type": "string"},
                "quantity": {"type": "integer", "min": 1},
            }
        )
        if v.validate(value):
            return value
        else:
            raise ValueError(json.dumps(v.errors))

    parser = reqparse.RequestParser()
    parser.add_argument("payment_method", type=str)
    parser.add_argument("total_paid", type=float)
    parser.add_argument("items", type=order_validator, action="append")

    def get(self, *, _id: str | None = None) -> tuple[dict, int]:
        if _id:
            order = (
                db.session.query(Order).where(Order.id == _id).one_or_none()
            )
            if order:
                return OrderDTO.from_model(order), 200
            return {"message": "Order was not found"}, 404
        orders = db.session.query(Order).all()
        return OrderDTO.from_model_list(orders), 200

    def post(self):
        # msg, code = super().authenticate(admin_only=True)
        # if code != 200:
        #     return msg, code
        data = OrderResource.parser.parse_args()
        new_order = Order(
            payment_method=PaymentMethodType[data["payment_method"]],
            total_paid=data["total_paid"],
        )
        # Group items by department
        for item in data["items"]:
            department = (
                db.session.query(Item)
                .filter_by(id=item["item_id"])
                .one_or_none()
                .department
            )
            if department in new_order.order_departments:
                new_order.departments_orders[
                    new_order.order_departments.index(department)
                ].department_order_items.append(
                    DepartmentOrderItem(
                        item=(
                            db.session.query(Item)
                            .filter_by(id=item["item_id"])
                            .one_or_none()
                        ),
                        quantity=item["quantity"],
                    )
                )
            else:
                new_order.departments_orders.append(
                    DepartmentOrder(
                        department=department,
                        department_order_items=[
                            DepartmentOrderItem(
                                item=(
                                    db.session.query(Item)
                                    .filter_by(id=item["item_id"])
                                    .one_or_none()
                                ),
                                quantity=item["quantity"],
                            )
                        ],
                    )
                )
        db.session.add(new_order)
        db.session.commit()
        return OrderDTO.from_model(new_order), 201


#   $ curl -X POST http://127.0.0.1:5000/api/v1/orders -H "Content-Type: application/json" -d '{"payment_method": "CASH", "total_paid": 50, "items": [{"item_id": "031396d8-00a1-11f0-a44e-0242ac120003", "quantity": 2}, {"item_id": "0313976e-00a1-11f0-a44e-0242ac120003", "quantity": 3}, {"item_id": "03139804-00a1-11f0-a44e-0242ac120003", "quantity": 1}]}'
