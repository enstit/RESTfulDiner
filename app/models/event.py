# app/models/event.py


from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd
from app.models._types import EventType

from app.utils import uuid8


class Event(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="Event"),
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

    days: Mapped[List["EventDay"]] = relationship(  # type: ignore # noqa: F821
        "EventDay", back_populates="event"
    )
    kiosks: Mapped[List["Kiosk"]] = relationship(  # type: ignore # noqa: F821
        "Kiosk", back_populates="event"
    )
    delivery_stations: Mapped[List["DeliveryStation"]] = relationship(  # type: ignore # noqa: F821
        "DeliveryStation", back_populates="event"
    )
    printers: Mapped[List["Printer"]] = relationship(  # type: ignore # noqa: F821
        "Printer", back_populates="event"
    )
    departments: Mapped[List["Department"]] = relationship(  # type: ignore # noqa: F821
        "Department", back_populates="event"
    )
