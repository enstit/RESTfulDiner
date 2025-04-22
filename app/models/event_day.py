# app/models/event_day.py

from typing import List
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class EventDay(BaseModel):
    event__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("event.id"),
        nullable=False,
        comment="Event identifier",
    )
    event_date: Mapped[date] = mapped_column(cd.DATE, comment="Event day date")
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
