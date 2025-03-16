# app/models/department.py


from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class Department(BaseModel):

    id = BaseModel.id
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME,
        unique=True,
        comment="Unique name of the department",
    )
    color: Mapped[Optional[str]] = mapped_column(
        cd.SHORT_NAME,
        comment="Department color",
    )
    printer__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        ForeignKey("printer.id"),
        nullable=True,
        default=None,
        comment="Printer identifier associated with the department",
    )

    printer = relationship("Printer", back_populates="department")
    items = relationship("Item", back_populates="department")
    department_orders = relationship(
        "DepartmentOrder", back_populates="department"
    )
