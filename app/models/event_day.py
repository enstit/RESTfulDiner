# app/models/event_day.py


from typing import List
from datetime import date

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class EventDay(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Event identifier",
    )
    event_day_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="EventDay"),
        primary_key=True,
        comment="Unique Event identifier",
    )
    event_day_date: Mapped[date] = mapped_column(
        cd.DATE, comment="Event day date"
    )
    start_datetime: Mapped[str] = mapped_column(
        cd.DATETIME, comment="Event day start date and time"
    )
    end_datetime: Mapped[str] = mapped_column(
        cd.DATETIME, comment="Event day end date and time"
    )

    event: Mapped["Event"] = relationship(  # type: ignore # noqa: F821
        "Event", back_populates="days"
    )
    orders: Mapped[List["Order"]] = relationship(  # type: ignore # noqa: F821
        "Order", back_populates="event_day"
    )

    __table_args__ = (ForeignKeyConstraint([event_id], ["event.event_id"]),)
