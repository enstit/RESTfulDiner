# app/models/__init__.py


from sqlalchemy import MetaData

metadata = MetaData()

from app.models._base import BaseModel as Diner
from app.models.delivery_station import DeliveryStation
from app.models.department import Department
from app.models.department_order import DepartmentOrder
from app.models.department_order_item import DepartmentOrderItem
from app.models.item import Item
from app.models.kiosk import Kiosk
from app.models.order import Order
from app.models.printer import Printer
from app.models.user import User

__all__ = [
    "Diner",
    "DeliveryStation",
    "Department",
    "DepartmentOrder",
    "DepartmentOrderItem",
    "Item",
    "Kiosk",
    "Order",
    "Printer",
    "User",
]
