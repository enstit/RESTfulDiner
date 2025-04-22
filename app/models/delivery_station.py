# app/models/delivery_station.py


from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class DeliveryStation(BaseModel):
    event__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("event.id"),
        nullable=False,
        comment="Event identifier",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, comment="Unique delivery station name"
    )
    active_flag: Mapped[bool] = mapped_column(
        cd.FLAG,
        default=True,
        comment="Whether the delivery station is active or not",
    )

    event: Mapped["Event"] = relationship(  # type: ignore # noqa: F821
        "Event", back_populates="delivery_stations"
    )
    orders: Mapped[List["Order"]] = relationship(  # type: ignore # noqa: F821
        "Order", back_populates="delivery_station"
    )

    __table_args__ = (
        UniqueConstraint(
            "event__id", "name", name="uq_event_delivery_station"
        ),
        {
            "comment": "Event Delivery Station",
            "extend_existing": True,
        },
    )
