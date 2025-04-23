# app/models/sys_shift.py

from datetime import datetime

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class SysShift(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Event identifier associated with the shift in the event day",
    )
    shift_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="SysShift"),
        primary_key=True,
        comment="Shift identifier associated with the user shift in the event day",
    )
    user_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        comment="User identifier associated with the user shift in the event day",
    )
    login_datetime: Mapped[datetime] = mapped_column(
        cd.DATETIME,
        server_default=func.now(),
        comment="Date and time of the user login in the shift",
    )
    logout_datetime: Mapped[datetime] = mapped_column(
        cd.DATETIME,
        nullable=True,
        server_onupdate=func.now(),
        comment="Date and time of the user logout in the shift",
    )
    token: Mapped[str] = mapped_column(
        cd.TEXT,
        nullable=True,
        comment="Token used for the user login in the shift",
    )

    event: Mapped["CfgEvent"] = relationship(  # type: ignore # noqa: F821
        "CfgEvent", back_populates="shifts"
    )
    user: Mapped["CfgUser"] = relationship(  # type: ignore # noqa: F821
        "CfgUser", back_populates="shifts"
    )

    __table_args__ = (
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
        ForeignKeyConstraint([user_id], ["cfg_user.user_id"]),
    )
