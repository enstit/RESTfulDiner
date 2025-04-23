# app/models/cfg_event.py


from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd
from app.models._types import EventType

from app.utils import uuid8


class CfgEvent(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="CfgEvent"),
        primary_key=True,
        comment="Unique Event identifier",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, unique=True, comment="Event name"
    )
    description: Mapped[str] = mapped_column(
        cd.TEXT, nullable=True, comment="Event description"
    )
    location: Mapped[str] = mapped_column(
        cd.TEXT, nullable=True, comment="Event location"
    )
    event_type: Mapped[EventType] = mapped_column(
        cd.CHOICE(EventType),
        default=EventType.SAGRA,
        comment=(
            "Event type: one between "
            + ", ".join([eventtype.desc for eventtype in EventType])
        ),
    )

    days: Mapped[List["CfgEventDay"]] = relationship(  # type: ignore # noqa: F821
        "CfgEventDay", back_populates="event"
    )
    kiosks: Mapped[List["CfgKiosk"]] = relationship(  # type: ignore # noqa: F821
        "CfgKiosk", back_populates="event"
    )
    delivery_stations: Mapped[List["CfgDeliveryStation"]] = relationship(  # type: ignore # noqa: F821
        "CfgDeliveryStation", back_populates="event"
    )
    printers: Mapped[List["CfgPrinter"]] = relationship(  # type: ignore # noqa: F821
        "CfgPrinter", back_populates="event"
    )
    departments: Mapped[List["CfgDepartment"]] = relationship(  # type: ignore # noqa: F821
        "CfgDepartment", back_populates="event"
    )
    shifts: Mapped[List["SysShift"]] = relationship(  # type: ignore # noqa: F821
        "SysShift", back_populates="event"
    )
