# app/models/printer.py


from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models._types import ColumnsDomains as cd
from app.models._base import BaseModel


class Printer(BaseModel):

    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, unique=True, comment="Unique printer name"
    )
    mac_address: Mapped[Optional[str]] = mapped_column(
        cd.TEXT, unique=True, comment="Printer MAC address"
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        cd.IP_ADDRESS, unique=True, comment="Printer IP address"
    )

    kiosk: Mapped["Kiosk"] = relationship(  # noqa: F821 # type: ignore
        "Kiosk", back_populates="printer"
    )
    department = relationship("Department", back_populates="printer")
