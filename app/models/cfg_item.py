# app/models/cfg_item.py


from typing import List, Optional

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import AllergenType, MenuSectionType, OrderStatusType
from app.models._types import ColumnsDomains as cd

from app.utils import uuid8


class CfgItem(BaseModel):
    event_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        primary_key=True,
        comment="Unique Event identifier to which the Item belongs",
    )
    item_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="CfgItem"),
        primary_key=True,
        comment="Unique Item identifier for the event",
    )
    name: Mapped[str] = mapped_column(
        cd.SHORT_NAME,
        comment="Unique name of the item",
    )
    description: Mapped[Optional[str]] = mapped_column(
        cd.TEXT,
        nullable=True,
        comment="Description of the item",
    )
    department_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
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
        cd.MONEY, comment="Item price, in euros"
    )
    deposit: Mapped[Optional[float]] = mapped_column(
        cd.MONEY,
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

    department: Mapped["CfgDepartment"] = relationship(  # type: ignore # noqa: F821
        "CfgDepartment", back_populates="items"
    )
    departments_orders_items: Mapped[List["SysOrderDepartmentItem"]] = (  # type: ignore # noqa: F821
        relationship("SysOrderDepartmentItem", back_populates="item")
    )

    __table_args__ = (
        ForeignKeyConstraint([event_id], ["cfg_event.event_id"]),
        ForeignKeyConstraint(
            [event_id, department_id],
            ["cfg_department.event_id", "cfg_department.department_id"],
        ),
        UniqueConstraint("event_id", "name"),
    )
