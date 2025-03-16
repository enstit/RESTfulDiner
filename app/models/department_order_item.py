# app/models/department_order_item.py


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class DepartmentOrderItem(BaseModel):

    id = BaseModel.id
    department_order__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("department_order.id"),
        comment="Order identifier associated with the department order",
    )
    item__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("item.id"),
        comment="Item identifier associated with the item",
    )
    quantity: Mapped[int] = mapped_column(
        cd.INT, default=1, comment="Item quantity"
    )

    department_order = relationship(
        "DepartmentOrder", back_populates="department_order_items"
    )
    item = relationship("Item", back_populates="departments_orders_items")

    @hybrid_property
    def total_price(self):
        return self.item.price * self.quantity
