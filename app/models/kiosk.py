# app/models/kiosk.py


from typing import Optional, List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class Kiosk(BaseModel):
    event__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("event.id"),
        nullable=False,
        comment="Event identifier",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, comment="Unique kiosk name"
    )
    printer__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        ForeignKey("printer.id"),
        nullable=True,
        comment="Printer identifier associated with the kiosk",
    )
    printer: Mapped["Printer"] = relationship(  # noqa: F821 # type: ignore
        "Printer", back_populates="kiosk"
    )

    event: Mapped["Event"] = relationship(  # noqa: F821 # type: ignore
        "Event", back_populates="kiosks"
    )
    orders: Mapped[List["Order"]] = relationship(  # noqa: F821 # type: ignore
        "Order", back_populates="kiosk"
    )

    __table_args__ = (
        UniqueConstraint("event__id", "name", name="uq_event_kiosk"),
        {
            "comment": "Event Kiosk for order management",
            "extend_existing": True,
        },
    )
