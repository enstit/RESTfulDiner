# app/models/department.py

from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class Department(BaseModel):
    event__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("event.id"),
        nullable=False,
        comment="Event identifier associated with the department",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME,
        unique=True,
        comment="Unique name of the department",
    )
    color: Mapped[Optional[str]] = mapped_column(
        cd.SHORT_NAME,
        comment=(
            "A color between the Recognized color keyword names. "
            "See also https://www.w3.org/TR/SVG11/types.html#ColorKeywords"
        ),
    )
    printer__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        ForeignKey("printer.id"),
        nullable=True,
        default=None,
        comment="Identifier of the printer the department is equipped with",
    )

    event: Mapped["Event"] = relationship(  # type: ignore # noqa: F821
        "Event", back_populates="departments"
    )
    printer: Mapped["Printer"] = relationship(  # type: ignore # noqa: F821
        "Printer", back_populates="department"
    )
    items: Mapped[List["Item"]] = relationship(  # type: ignore # noqa: F821
        "Item", back_populates="department"
    )
    department_orders: Mapped[List["DepartmentOrder"]] = relationship(  # type: ignore # noqa: F821
        "DepartmentOrder", back_populates="department"
    )
