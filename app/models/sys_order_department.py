# app/models/sys_order_department.py

from typing import List

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd
from app.models._types import OrderStatusType


class SysOrderDepartment(BaseModel):
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
    current_status: Mapped[OrderStatusType] = mapped_column(
        cd.CHOICE(OrderStatusType),
        default=OrderStatusType.COMPLETED,
        comment=(
            "Current status of the department order: one between "
            + ", ".join([status.desc for status in OrderStatusType])
        ),
    )

    department: Mapped["CfgDepartment"] = relationship(  # type: ignore # noqa: F821
        "CfgDepartment", back_populates="department_orders"
    )
    order: Mapped["SysOrder"] = relationship(  # type: ignore # noqa: F821
        "SysOrder", back_populates="departments_orders"
    )
    department_order_items: Mapped[List["SysOrderDepartmentItem"]] = (  # type: ignore # noqa: F821
        relationship(
            "SysOrderDepartmentItem", back_populates="department_order"
        )
    )

    @hybrid_property
    def total_price(self):
        return sum(
            [
                department_order_item.total_price
                for department_order_item in self.department_order_items
            ]
        )

    __table_args__ = (
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
        ForeignKeyConstraint(
            [event_id, order_id],
            ["sys_order.event_id", "sys_order.order_id"],
        ),
        ForeignKeyConstraint(
            [event_id, department_id],
            ["cfg_department.event_id", "cfg_department.department_id"],
        ),
    )
