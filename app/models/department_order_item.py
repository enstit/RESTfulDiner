# app/models/department_order_item.py


from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class DepartmentOrderItem(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Event identifier associated with the order in a specific Department",
    )
    order_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Order identifier associated with the order in a specific Department",
    )
    department_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Department identifier associated with the order in a specific Department",
    )
    item_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Item identifier associated with the order in a specific Department",
    )
    quantity: Mapped[int] = mapped_column(
        cd.INT, default=1, comment="Item quantity"
    )

    department_order: Mapped["DepartmentOrder"] = relationship(  # type: ignore # noqa: F821
        "DepartmentOrder", back_populates="department_order_items"
    )
    item: Mapped["Item"] = relationship(  # type: ignore # noqa: F821
        "Item", back_populates="departments_orders_items"
    )

    @hybrid_property
    def total_price(self):
        return self.item.price * self.quantity

    __table_args__ = (
        ForeignKeyConstraint([event_id], ["event.event_id"]),
        ForeignKeyConstraint(
            [event_id, department_id],
            ["department.event_id", "department.department_id"],
        ),
        ForeignKeyConstraint(
            [event_id, order_id], ["order.event_id", "order.order_id"]
        ),
        ForeignKeyConstraint(
            [event_id, item_id],
            ["item.event_id", "item.item_id"],
        ),
        ForeignKeyConstraint(
            [event_id, order_id, department_id],
            [
                "department_order.event_id",
                "department_order.order_id",
                "department_order.department_id",
            ],
        ),
    )
