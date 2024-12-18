from sqlalchemy.orm import Mapped, mapped_column

from ._base import BaseModel
from ._types import ColumnsDomains as cd
from ._types import UserRoleType


class User(BaseModel):

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
