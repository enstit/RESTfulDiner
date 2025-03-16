# app/models/delivery_station.py


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd


class DeliveryStation(BaseModel):

    id = BaseModel.id
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME, unique=True, comment="Unique delivery station name"
    )
    active_flag: Mapped[bool] = mapped_column(
        cd.FLAG,
        default=True,
        comment="Whether the delivery station is active or not",
    )

    orders = relationship("Order", back_populates="delivery_station")
