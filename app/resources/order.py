# app/resources/order.py

import json
from datetime import datetime

from cerberus import Validator
from flask_restful import reqparse

from app.dto.order import OrderDTO, DepartmentOrderDTO
from app.extensions import db
from app.models.sys_order_department import SysOrderDepartment
from app.models.sys_order_department_item import SysOrderDepartmentItem
from app.models.cfg_event_day import CfgEventDay
from app.models.cfg_item import CfgItem
from app.models.sys_order import SysOrder, PaymentMethodType
from app.models._types import OrderStatusType
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

    def get(
        self, *, order_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if order_id:
            order = (
                db.session.query(SysOrder)
                .filter(
                    SysOrder.event_id == msg.get("event_id"),
                    SysOrder.order_id == order_id,
                )
                .one_or_none()
            )
            if order:
                return OrderDTO.from_model(order), 200
            return {
                "error": f"Order {order_id} was not found in the current event"
            }, 404
        orders = (
            db.session.query(SysOrder)
            .filter(SysOrder.event_id == msg.get("event_id"))
            .all()
        )
        return OrderDTO.from_model_list(orders), 200

    def post(self):
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        data = OrderResource.parser.parse_args()
        # Get the EventDay from the current datetime
        event_day = (
            db.session.query(CfgEventDay)
            .filter(
                CfgEventDay.event_id == msg.get("event_id"),
                CfgEventDay.start_datetime <= datetime.now(),
                CfgEventDay.end_datetime > datetime.now(),
            )
            .one_or_none()
        )
        if event_day is None:
            return {
                "error": "There are no events at the current time for the current event"
            }, 400
        # Create a new empty order, to which we will add DepartmentsOrders
        new_order = SysOrder(
            payment_method=PaymentMethodType[data["payment_method"]],
            event_day=event_day,
            total_paid=data["total_paid"],
            user_id=msg.get("user_id"),
            kiosk_id=msg.get("kiosk_id"),
        )
        # Group items by department
        if data["items"] is not None:
            for item in data["items"]:
                department = (
                    db.session.query(CfgItem)
                    .filter(
                        CfgItem.event_id == msg.get("event_id"),
                        CfgItem.item_id == item["item_id"],
                    )
                    .one()
                    .department
                )
                if department in new_order.departments:
                    new_order.departments_orders[
                        new_order.departments.index(department)
                    ].department_order_items.append(
                        SysOrderDepartmentItem(
                            item=(
                                db.session.query(CfgItem)
                                .filter(
                                    CfgItem.event_id == msg.get("event_id"),
                                    CfgItem.item_id == item["item_id"],
                                )
                                .one_or_none()
                            ),
                            quantity=item["quantity"],
                        )
                    )
                else:
                    new_order.departments_orders.append(
                        SysOrderDepartment(
                            department=department,
                            department_order_items=[
                                SysOrderDepartmentItem(
                                    item=(
                                        db.session.query(CfgItem)
                                        .filter(
                                            CfgItem.event_id
                                            == msg.get("event_id"),
                                            CfgItem.item_id == item["item_id"],
                                        )
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


class DepartmentOrderResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("current_status", type=str)

    def get(
        self, department_id: str, *, order_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        """Get all orders for a specific department in the event"""
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if order_id:
            department_order = (
                db.session.query(SysOrderDepartment)
                .filter(
                    SysOrderDepartment.event_id == msg.get("event_id"),
                    SysOrderDepartment.department_id == department_id,
                    SysOrderDepartment.order_id == order_id,
                )
                .one_or_none()
            )
            if department_order:
                return DepartmentOrderDTO.from_model(department_order), 200
            return {
                "error": f"Department order {order_id} for department {department_id} was not found in the current event"
            }, 404
        department_orders = (
            db.session.query(SysOrderDepartment)
            .filter(
                SysOrderDepartment.event_id == msg.get("event_id"),
                SysOrderDepartment.department_id == department_id,
                # Filter out cancelled and completed orders, to only keep
                # the ones that are in progress or not started yet
                SysOrderDepartment.current_status != OrderStatusType.CANCELLED,
                SysOrderDepartment.current_status != OrderStatusType.COMPLETED,
            )
            .all()
        )
        if department_orders:
            return DepartmentOrderDTO.from_model_list(department_orders), 200
        return {
            "error": f"Department orders for department {department_id} were not found in the current event"
        }, 404

    def patch(self, department_id: str, order_id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        data = DepartmentOrderResource.parser.parse_args()
        department_order = (
            db.session.query(SysOrderDepartment)
            .filter(
                SysOrderDepartment.event_id == msg.get("event_id"),
                SysOrderDepartment.department_id == department_id,
                SysOrderDepartment.order_id == order_id,
            )
            .one_or_none()
        )
        if not department_order:
            return {
                "error": f"Department order {order_id} in department {department_id} was not found in the current event"
            }, 404
        if "current_status" in data and data["current_status"]:
            department_order.current_status = OrderStatusType[
                data["current_status"]
            ]
        db.session.commit()
        return DepartmentOrderDTO.from_model(department_order), 200
