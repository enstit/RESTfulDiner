# app/models/cfg_delivery_station.py


from typing import List

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class CfgDeliveryStation(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Unique Event identifier to which the Delivery Station belongs",
    )
    delivery_station_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="CfgDeliveryStation"),
        primary_key=True,
        comment="Unique Delivery Station identifier for the event",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, comment="Unique Delivery Station name for the event"
    )
    active_flag: Mapped[bool] = mapped_column(
        cd.FLAG,
        default=True,
        comment="Whether the Delivery Station is active or not",
    )

    event: Mapped["CfgEvent"] = relationship(  # type: ignore # noqa: F821
        "CfgEvent", back_populates="delivery_stations"
    )
    orders: Mapped[List["SysOrder"]] = relationship(  # type: ignore # noqa: F821
        "SysOrder", back_populates="delivery_station"
    )

    __table_args__ = (
        UniqueConstraint("event_id", "name"),
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
    )
