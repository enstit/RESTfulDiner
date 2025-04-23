# app/models/order.py


from typing import Optional, List
from datetime import datetime

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd
from app.models._types import PaymentMethodType

from app.utils import uuid8


class Order(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Event identifier associated with the order",
    )
    order_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="Kiosk"),
        primary_key=True,
        comment="Unique Order identifier for the event",
    )
    event_day_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        nullable=False,
        comment="Event day identifier associated with the order",
    )
    seq_no: Mapped[int] = mapped_column(
        cd.POS,
        nullable=True,
        comment="Order sequence number, unique for the event day",
    )
    created_datetime: Mapped[datetime] = mapped_column(
        cd.DATETIME,
        server_default=func.now(),
        comment="Order creation datetime",
    )
    user__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        comment="User identifier associated with the order",
    )
    kiosk__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
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
        nullable=True,
        comment="Delivery station identifier associated with the order",
    )

    event_day: Mapped["EventDay"] = relationship(  # type: ignore # noqa: F821
        "EventDay", back_populates="orders"
    )
    kiosk: Mapped["Kiosk"] = relationship(  # type: ignore # noqa: F821
        "Kiosk", back_populates="orders"
    )
    user: Mapped["User"] = relationship(  # type: ignore # noqa: F821
        "User", back_populates="orders"
    )
    delivery_station: Mapped["DeliveryStation"] = relationship(  # type: ignore # noqa: F821
        "DeliveryStation", back_populates="orders"
    )
    departments_orders: Mapped[List["DepartmentOrder"]] = relationship(  # type: ignore # noqa: F821
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
    def total_charge(self) -> float:
        """Return the total charge of the order, if the order has a total paid
        amount, in the system currency"""
        return self.total_paid - self.total_price if self.total_paid else 0

    @hybrid_property
    def order_departments(self) -> list["Department"]:  # type: ignore # noqa: F821
        """Return the list of departments associated with the order"""
        return [
            department_order.department
            for department_order in self.departments_orders
        ]

    __table_args__ = (
        UniqueConstraint(event_id, event_day_id, seq_no),
        ForeignKeyConstraint([event_id], ["event.event_id"]),
        ForeignKeyConstraint(
            [event_id, event_day_id],
            ["event_day.event_id", "event_day.event_day_id"],
        ),
        ForeignKeyConstraint(
            [event_id, kiosk__id], ["kiosk.event_id", "kiosk.kiosk_id"]
        ),
        ForeignKeyConstraint(
            [event_id, delivery_station__id],
            [
                "delivery_station.event_id",
                "delivery_station.delivery_station_id",
            ],
        ),
        ForeignKeyConstraint([user__id], ["user.user_id"]),
        {
            "comment": "Order for the event",
            "extend_existing": True,
        },
    )
