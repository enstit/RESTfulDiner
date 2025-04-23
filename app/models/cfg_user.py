# app/models/cfg_user.py


from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.models._base import BaseModel
from app.models._types import ColumnsDomains as cd
from app.models._types import UserRoleType

from app.utils import uuid8


class CfgUser(BaseModel):
    user_id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=lambda: uuid8(domain="CfgUser"),
        primary_key=True,
        comment="Unique User identifier for the system",
    )
    username: Mapped[str] = mapped_column(
        cd.SHORT_NAME, unique=True, comment="Unique username"
    )
    password: Mapped[str] = mapped_column(
        cd.PASSWORD,
        nullable=True,
        default=None,
        comment="User password",
    )
    role: Mapped[UserRoleType] = mapped_column(
        cd.CHOICE(UserRoleType),
        default=UserRoleType.OPERATOR,
        comment=(
            "User role: one between "
            + ", ".join([role.desc for role in UserRoleType])
        ),
    )

    orders: Mapped[List["SysOrder"]] = relationship(  # type: ignore # noqa: F821
        "SysOrder", back_populates="user"
    )
    shifts: Mapped[List["SysShift"]] = relationship(  # type: ignore # noqa: F821
        "SysShift", back_populates="user"
    )
