# app/models/sys_order_department_item.py


from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class SysOrderDepartmentItem(BaseModel):
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

    department_order: Mapped["SysOrderDepartment"] = relationship(  # type: ignore # noqa: F821
        "SysOrderDepartment", back_populates="department_order_items"
    )
    item: Mapped["CfgItem"] = relationship(  # type: ignore # noqa: F821
        "CfgItem", back_populates="departments_orders_items"
    )

    @hybrid_property
    def total_price(self):
        return self.item.price * self.quantity

    __table_args__ = (
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
        ForeignKeyConstraint(
            [event_id, department_id],
            ["cfg_department.event_id", "cfg_department.department_id"],
        ),
        ForeignKeyConstraint(
            [event_id, order_id], ["sys_order.event_id", "sys_order.order_id"]
        ),
        ForeignKeyConstraint(
            [event_id, item_id],
            ["cfg_item.event_id", "cfg_item.item_id"],
        ),
        ForeignKeyConstraint(
            [event_id, order_id, department_id],
            [
                "sys_order_department.event_id",
                "sys_order_department.order_id",
                "sys_order_department.department_id",
            ],
        ),
    )
