# app/models/cfg_kiosk.py


from typing import Optional, List

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class CfgKiosk(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Unique Event identifier to which the Kiosk belongs",
    )
    kiosk_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="CfgKiosk"),
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
    printer: Mapped["CfgPrinter"] = relationship(  # noqa: F821 # type: ignore
        "CfgPrinter", back_populates="kiosk"
    )

    event: Mapped["CfgEvent"] = relationship(  # noqa: F821 # type: ignore
        "CfgEvent", back_populates="kiosks"
    )
    orders: Mapped[List["SysOrder"]] = (  # noqa: F821 # type: ignore
        relationship("SysOrder", back_populates="kiosk")
    )

    __table_args__ = (
        UniqueConstraint("event_id", "name"),
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
        ForeignKeyConstraint(
            [event_id, printer_id],
            ["cfg_printer.event_id", "cfg_printer.printer_id"],
        ),
    )
