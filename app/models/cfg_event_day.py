# app/models/cfg_event_day.py


from typing import List
from datetime import date

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class CfgEventDay(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Event identifier",
    )
    event_day_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="CfgEventDay"),
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

    event: Mapped["CfgEvent"] = relationship(  # type: ignore # noqa: F821
        "CfgEvent", back_populates="days"
    )
    orders: Mapped[List["SysOrder"]] = relationship(  # type: ignore # noqa: F821
        "SysOrder", back_populates="event_day"
    )

    __table_args__ = (
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
    )
