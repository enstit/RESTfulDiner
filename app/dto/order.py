# app/dto/order.py


from typing import List

from app.config import Config
from app.models.order import Order
from app.models.department_order_item import DepartmentOrderItem


class OrderItemDTO:

    def __init__(self, department_order_item: DepartmentOrderItem):
        self.item = department_order_item.item
        self.quantity = department_order_item.quantity

    def to_dict(self) -> dict:
        return {
            "type": "schema:Order",
            "item": f"{Config.APP_URL}{Config.API_URI}/items/{self.item.id}",
            "quantity": self.quantity,
        }


class OrderDTO:

    CONTEXT = {
        "@context": {
            "schema": "https://schema.org/",
            "self": "@id",
            "type": "@type",
            "created_datetime": "schema:orderDate",
            "kiosk": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "payment_method": "schema:paymentMethod",
            "total_price": "schema:price",
            "total_paid": "schema:price",
            "total_charge": "schema:price",
            "delivery_station": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "items": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "license": {"@id": "schema:license", "@type": "@id"},
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    def __init__(self, order: Order):
        self.id = order.id
        self.created_datetime = order.created_datetime
        self.kiosk = order.kiosk
        self.payment_method = order.payment_method
        self.total_price = round(order.total_price, 2)
        self.total_paid = round(order.total_paid, 2)
        self.total_charge = round(order.total_charge, 2)
        self.delivery_station = order.delivery_station
        self.items = [
            OrderItemDTO(department_order_item)
            for department_order in order.departments_orders
            for department_order_item in department_order.department_order_items
        ]

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/orders/{self.id}",
            "type": "schema:Order",
            "created_datetime": self.created_datetime.isoformat(),
            "kiosk": (
                f"{Config.APP_URL}{Config.API_URI}/kiosks/{self.kiosk.id}"
                if self.kiosk
                else None
            ),
            "payment_method": self.payment_method.name,
            "total_price": self.total_price,
            "total_paid": self.total_paid,
            "total_charge": self.total_charge,
            "delivery_station": (
                f"{Config.APP_URL}{Config.API_URI}/delivery_stations/{self.delivery_station.id}"
                if self.delivery_station
                else None
            ),
            "items": [item.to_dict() for item in self.items],
        }

    @staticmethod
    def from_model(order: Order) -> dict:
        return {
            **OrderDTO.CONTEXT,
            "data": OrderDTO(order).to_dict() if order else None,
        }

    @staticmethod
    def from_model_list(orders: List[Order]) -> dict:
        return {
            **OrderDTO.CONTEXT,
            "data": [OrderDTO(order).to_dict() for order in orders],
        }
