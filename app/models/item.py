from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy_utils import UUIDType

from ._base import BaseModel
from ._types import ColumnsDomains as cd
from ._types import AllergenType
from ._types import OrderStatusType
from ._types import MenuSectionType


class Item(BaseModel):

    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME,
        unique=True,
        comment="Unique name of the item",
    )
    description: Mapped[Optional[str]] = mapped_column(
        cd.TEXT,
        nullable=True,
        comment="Description of the item",
    )
    department__id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        ForeignKey("department.id"),
        nullable=False,
        comment="Department identifier associated with the item",
    )
    menu_section: Mapped[MenuSectionType] = mapped_column(
        cd.CHOICE(MenuSectionType),
        nullable=False,
        comment=(
            "Menu section identifier associated with the item: one between "
            + ", ".join([menusection.desc for menusection in MenuSectionType])
        ),
    )
    price: Mapped[float] = mapped_column(
        cd.DECIMAL, comment="Item price, in euros"
    )
    deposit: Mapped[Optional[float]] = mapped_column(
        cd.DECIMAL,
        nullable=True,
        default=None,
        comment="Item deposit price, if present, in euros",
    )
    availability: Mapped[int] = mapped_column(
        cd.INT,
        nullable=True,
        default=None,
        comment="Item availability",
    )
    initial_status: Mapped[OrderStatusType] = mapped_column(
        cd.CHOICE(OrderStatusType),
        default=OrderStatusType.COMPLETED,
        comment=(
            "Initial status of the item: one between "
            + ", ".join([status.desc for status in OrderStatusType])
        ),
    )
    visible_flag: Mapped[bool] = mapped_column(
        cd.FLAG,
        default=True,
        comment="Whether the item is visible or not",
    )
    allergens: Mapped[List[AllergenType]] = mapped_column(
        ARRAY(cd.CHOICE(AllergenType)),
        nullable=True,
        default=None,
        comment=(
            "List of allergens associated with the item: possible values are "
            + ", ".join([allergen.desc for allergen in AllergenType])
        ),
    )

    department = relationship("Department", back_populates="items")
    departments_orders_items = relationship(
        "DepartmentOrderItem", back_populates="item"
    )
