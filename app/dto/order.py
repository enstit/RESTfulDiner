# app/dto/order.py

from typing import List

from app.config import Config
from app.models.order import Order
from app.models.department_order import DepartmentOrder
from app.models.department_order_item import DepartmentOrderItem


class DepartmentOrderItemDTO:

    def __init__(self, department_order_item: DepartmentOrderItem):
        self.item = department_order_item.item
        self.quantity = department_order_item.quantity

    def to_dict(self) -> dict:
        return {
            "type": "schema:Order",
            "item": f"{Config.APP_URL}{Config.API_URI}/items/{self.item.id}",
            "quantity": self.quantity,
        }


class DepartmentOrderDTO:

    def __init__(self, department_order: DepartmentOrder):
        self.department = department_order.department
        self.current_status = department_order.current_status
        self.department_order_items = [
            DepartmentOrderItemDTO(department_order_item)
            for department_order_item in department_order.department_order_items
        ]

    def to_dict(self) -> dict:
        return {
            "type": "schema:Order",
            "department": f"{Config.APP_URL}{Config.API_URI}/departments/{self.department.id}",
            "current_status": self.current_status,
            "department_order_items": [
                department_order_item.to_dict()
                for department_order_item in self.department_order_items
            ],
        }


class OrderDTO:

    CONTEXT = {
        "@context": {
            "schema": "https://schema.org/",
            "self": "@id",
            "type": "@type",
            "created_datetime": "schema:orderDate",
            "kiosk": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "is_deleted": "schema:archived",
            "payment_method": "schema:paymentMethod",
            "total_paid": "schema:price",
            "delivery_station": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "department_orders": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "department": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "current_status": "schema:orderStatus",
            "department_order_items": {
                "@id": "schema:isRelatedTo",
                "@type": "@id",
            },
            "item": "schema:Product",
            "quantity": "schema:amountOfThisGood",
            "license": {"@id": "schema:license", "@type": "@id"},
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    def __init__(self, order: Order):
        self.id = order.id
        self.created_datetime = order.created_datetime
        self.kiosk = order.kiosk
        self.is_deleted = order.deleted_flag
        self.payment_method = order.payment_method
        self.total_paid = order.total_paid
        self.delivery_station = order.delivery_station
        self.department_orders = [
            DepartmentOrderDTO(department_order)
            for department_order in order.department_orders
        ]

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/orders/{self.id}",
            "type": "schema:Order",
            "created_datetime": self.created_datetime,
            "kiosk": (
                f"{Config.APP_URL}{Config.API_URI}/kiosks/{self.kiosk.id}"
                if self.kiosk
                else None
            ),
            "is_deleted": self.is_deleted,
            "payment_method": self.payment_method.name,
            "total_paid": self.total_paid,
            "delivery_station": (
                f"{Config.APP_URL}{Config.API_URI}/delivery_stations/{self.delivery_station.id}"
                if self.delivery_station
                else None
            ),
            "department_orders": [
                department_order.to_dict()
                for department_order in self.department_orders
            ],
        }

    @staticmethod
    def from_model(order: Order) -> dict:
        return (
            {
                **OrderDTO.CONTEXT,
                "data": OrderDTO(order).to_dict(),
            }
            if order
            else None
        )

    @staticmethod
    def from_model_list(orders: List[Order]) -> dict:
        return {
            **OrderDTO.CONTEXT,
            "data": [OrderDTO(order).to_dict() for order in orders],
        }
