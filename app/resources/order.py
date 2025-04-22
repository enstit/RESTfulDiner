# app/resources/order.py

import json
from datetime import datetime

from cerberus import Validator
from flask_restful import reqparse

from app.dto.order import OrderDTO
from app.extensions import db
from app.models.department_order import DepartmentOrder
from app.models.department_order_item import DepartmentOrderItem
from app.models.event_day import EventDay
from app.models.item import Item
from app.models.order import Order, PaymentMethodType
from app.resources.auth import ProtectedResource


class OrderResource(ProtectedResource):
    @staticmethod
    def order_validator(value):
        v = Validator(
            {
                "item_id": {"required": True, "type": "string"},
                "quantity": {"type": "integer", "min": 1},
            }  # type: ignore
        )
        if v.validate(value):  # type: ignore
            return value
        else:
            raise ValueError(json.dumps(v.errors))  # type: ignore

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
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        data = OrderResource.parser.parse_args()
        # Get the EventDay from the current datetime
        event_day = (
            db.session.query(EventDay)
            .where(EventDay.event__id == msg.get("event_id"))
            .where(EventDay.start_datetime <= datetime.now())
            .where(EventDay.end_datetime > datetime.now())
            .one_or_none()
        )
        if event_day is None:
            return {"message": "There are no events at the current time"}, 400
        # Create a new empty order, to which we will add DepartmentsOrders
        new_order = Order(
            payment_method=PaymentMethodType[data["payment_method"]],
            event_day__id=event_day.id,
            total_paid=data["total_paid"],
            user__id=msg["user_id"],
            kiosk__id=msg.get("kiosk_id"),
        )
        # Group items by department
        if data["items"] is not None:
            for item in data["items"]:
                department = (
                    db.session.query(Item)
                    .where(Item.department.event__id == msg.get("event_id"))
                    .where(Item.id == item["item_id"])
                    .one()
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
