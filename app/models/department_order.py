# app/models/department_order.py

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd
from app.models._types import OrderStatusType


class DepartmentOrder(BaseModel):
    department__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("department.id"),
        comment="Department identifier associated with the item order",
    )
    order__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("order.id"),
        comment="Order identifier associated with the item order",
    )
    current_status: Mapped[OrderStatusType] = mapped_column(
        cd.CHOICE(OrderStatusType),
        default=OrderStatusType.COMPLETED,
        comment=(
            "Current status of the department order: one between "
            + ", ".join([status.desc for status in OrderStatusType])
        ),
    )

    department: Mapped["Department"] = relationship(  # type: ignore # noqa: F821
        "Department", back_populates="department_orders"
    )
    order: Mapped["Order"] = relationship(  # type: ignore # noqa: F821
        "Order", back_populates="departments_orders"
    )
    department_order_items: Mapped[List["DepartmentOrderItem"]] = relationship(  # type: ignore # noqa: F821
        "DepartmentOrderItem", back_populates="department_order"
    )

    @hybrid_property
    def total_price(self):
        return sum(
            [
                department_order_item.total_price
                for department_order_item in self.department_order_items
            ]
        )
