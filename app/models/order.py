# app/models/order.py


from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd
from app.models._types import PaymentMethodType


class Order(BaseModel):

    created_datetime: Mapped[datetime] = mapped_column(
        cd.DATETIME,
        server_default=func.now(),
        comment="Order creation datetime",
    )
    kiosk__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        ForeignKey("kiosk.id"),
        comment="Kiosk identifier associated with the order",
    )
    deleted_flag: Mapped[bool] = mapped_column(
        cd.FLAG,
        default=False,
        comment="Whether the order has been cancelled or not",
    )
    payment_method: Mapped[PaymentMethodType] = mapped_column(
        cd.CHOICE(PaymentMethodType),
        comment=(
            "Payment method: one between "
            + ", ".join([allergen.desc for allergen in PaymentMethodType])
        ),
    )
    total_paid: Mapped[float] = mapped_column(
        cd.MONEY,
        nullable=True,
        comment="Total amount paid, in euros",
    )
    delivery_station__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        ForeignKey("delivery_station.id"),
        nullable=True,
        comment="Delivery station identifier associated with the order",
    )

    kiosk = relationship("Kiosk", back_populates="orders")
    delivery_station = relationship("DeliveryStation", back_populates="orders")
    departments_orders = relationship(
        "DepartmentOrder", back_populates="order"
    )

    @hybrid_property
    def total_price(self) -> float:
        """Return the total price of the order, in the system currency"""
        return sum(
            department_order.total_price
            for department_order in self.departments_orders
        )

    @hybrid_property
    def total_charge(self) -> Optional[float]:
        """Return the total charge of the order, if the order has a total paid
        amount, in the system currency"""
        return self.total_paid - self.total_price if self.total_paid else None

    @hybrid_property
    def order_departments(self) -> list["Department"]:  # type: ignore # noqa: F821
        """Return the list of departments associated with the order"""
        return [
            department_order.department
            for department_order in self.departments_orders
        ]
