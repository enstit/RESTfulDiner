# app/models/kiosk.py


from typing import Optional, List

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class Kiosk(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Unique Event identifier to which the Kiosk belongs",
    )
    kiosk_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="Kiosk"),
        primary_key=True,
        comment="Unique Kiosk identifier for the event",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, comment="Unique Kiosk name"
    )
    printer_id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        nullable=True,
        comment="Printer identifier associated with the Kiosk",
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
        UniqueConstraint("event_id", "name"),
        ForeignKeyConstraint([event_id], ["event.event_id"]),
        ForeignKeyConstraint(
            [event_id, printer_id], ["printer.event_id", "printer.printer_id"]
        ),
        {
            "comment": "Event Kiosk for order management",
            "extend_existing": True,
        },
    )
