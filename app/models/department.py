# app/models/department.py

from typing import Optional, List

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class Department(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Unique Event identifier to which the Department belongs",
    )
    department_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="Department"),
        primary_key=True,
        comment="Unique Department identifier for the event",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME,
        comment="Unique name of the Department for the event",
    )
    color: Mapped[Optional[str]] = mapped_column(
        cd.SHORT_NAME,
        comment=(
            "A color between the Recognized color keyword names. "
            "See also https://www.w3.org/TR/SVG11/types.html#ColorKeywords"
        ),
    )
    printer_id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        nullable=True,
        default=None,
        comment="Identifier of the printer the Department is equipped with",
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

    __table_args__ = (
        UniqueConstraint("event_id", "name"),
        ForeignKeyConstraint([event_id], ["event.event_id"]),
        ForeignKeyConstraint(
            [event_id, printer_id], ["printer.event_id", "printer.printer_id"]
        ),
    )
