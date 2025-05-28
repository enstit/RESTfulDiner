# app/models/cfg_printer.py


from typing import Optional

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class CfgPrinter(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Unique Event identifier to which the Printer belongs",
    )
    printer_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="CfgPrinter"),
        primary_key=True,
        comment="Unique Printer identifier for the event",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, comment="Unique printer name"
    )
    mac_address: Mapped[Optional[str]] = mapped_column(
        cd.TEXT, comment="Printer MAC address"
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        cd.IP_ADDRESS, comment="Printer IP address"
    )

    event: Mapped["CfgEvent"] = relationship(  # noqa: F821
        "CfgEvent", back_populates="printers"
    )
    kiosk: Mapped[Optional["CfgKiosk"]] = relationship(  # noqa: F821
        "CfgKiosk", back_populates="printer"
    )
    department: Mapped[Optional["CfgDepartment"]] = relationship(  # noqa: F821
        "CfgDepartment", back_populates="printer"
    )

    __table_args__ = (
        UniqueConstraint("event_id", "name"),
        UniqueConstraint("event_id", "mac_address"),
        UniqueConstraint("event_id", "ip_address"),
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
    )
