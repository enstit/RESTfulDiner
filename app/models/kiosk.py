# app/models/kiosk.py


from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class Kiosk(BaseModel):

    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, unique=True, comment="Unique kiosk name"
    )
    printer__id: Mapped[Optional[UUIDType]] = mapped_column(
        cd.ID,
        ForeignKey("printer.id"),
        nullable=True,
        comment="Printer identifier associated with the kiosk",
    )
    printer: Mapped["Printer"] = relationship(  # noqa: F821 # type: ignore
        "Printer", back_populates="kiosk"
    )
    orders = relationship("Order", back_populates="kiosk")
