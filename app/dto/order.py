# app/dto/order.py


from typing import List

from app.config import Config
from app.models.order import Order
from app.models.department_order import DepartmentOrder
from app.models.department_order_item import DepartmentOrderItem


class OrderItemDTO:
    def __init__(self, department_order_item: DepartmentOrderItem):
        self.item_id = str(department_order_item.item_id)
        self.quantity = department_order_item.quantity

    def to_dict(self) -> dict:
        return {
            "item_url": f"{Config.APP_URL}{Config.API_URI}/items/{self.item_id}",
            "item_id": self.item_id,
            "quantity": self.quantity,
        }


class OrderDTO:
    def __init__(self, order: Order):
        self.event_id = str(order.event_id)
        self.order_id = str(order.order_id)
        self.created_datetime = order.created_datetime
        self.kiosk = order.kiosk
        self.user = order.user
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
            "self": f"{Config.APP_URL}{Config.API_URI}/orders/{self.order_id}",
            "type": "schema:Order",
            "created_datetime": self.created_datetime.isoformat(),
            "kiosk": (
                f"{Config.APP_URL}{Config.API_URI}/kiosks/{self.kiosk.kiosk_id}"
                if self.kiosk
                else None
            ),
            "user": self.user.username,
            "payment_method": self.payment_method.name,
            "total_price": self.total_price,
            "total_paid": self.total_paid,
            "total_charge": self.total_charge,
            "delivery_station": (
                f"{Config.APP_URL}{Config.API_URI}/delivery_stations/{self.delivery_station.delivery_station_id}"
                if self.delivery_station
                else None
            ),
            "items": [item.to_dict() for item in self.items],
        }

    @staticmethod
    def from_model(order: Order) -> dict:
        return OrderDTO(order).to_dict() if order else {}

    @staticmethod
    def from_model_list(orders: List[Order]) -> list[dict]:
        return [OrderDTO(order).to_dict() for order in orders]


class DepartmentOrderDTO:
    def __init__(self, department_order: DepartmentOrder):
        self.event_id = str(department_order.event_id)
        self.order_id = str(department_order.order_id)
        self.department_id = str(department_order.department_id)
        self.current_status = department_order.current_status
        self.delivery_station_id = str(
            department_order.order.delivery_station_id
        )
        self.items = [
            OrderItemDTO(department_order_item)
            for department_order_item in department_order.department_order_items
        ]

    def to_dict(self) -> dict:
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/departments/{self.department_id}/orders/{self.order_id}",
            "department_url": (
                f"{Config.APP_URL}{Config.API_URI}/departments/{self.department_id}"
            ),
            "current_status": self.current_status.name,
            "delivery_station_url": (
                f"{Config.APP_URL}{Config.API_URI}/delivery_stations/{self.delivery_station_id}"
                if self.delivery_station_id
                else None
            ),
            "items": [item.to_dict() for item in self.items],
        }

    @staticmethod
    def from_model(department_order: DepartmentOrder) -> dict:
        return (
            DepartmentOrderDTO(department_order).to_dict()
            if department_order
            else {}
        )

    @staticmethod
    def from_model_list(
        department_orders: List[DepartmentOrder],
    ) -> list[dict]:
        return [
            DepartmentOrderDTO(department_order).to_dict()
            for department_order in department_orders
        ]
