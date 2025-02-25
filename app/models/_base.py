import re

from pprint import pformat

from . import metadata
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy_utils import UUIDType

from uuid import uuid1 as uuid

from ._types import ColumnsDomains as cd


class BaseModel(DeclarativeBase):

    __abstract__ = True

    metadata = metadata

    id: Mapped[UUIDType] = mapped_column(
        cd.ID,
        default=uuid,
        primary_key=True,
        comment="Unique row identifier.",
    )

    # Automatically set the table name to the snake_case version of the
    # ClassName
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    def __repr__(self):
        """Return a string representation of the model instance, specifying the
        class name and the primary keys of the model instance."""
        return (
            f"{self.__class__.__name__}("
            f"""{
                ", ".join(
                    [
                        (
                            f'{pk}="{getattr(self, pk)}"'
                            if isinstance(getattr(self, pk), str)
                            else f"{pk}={getattr(self, pk)}"
                        )
                        for pk in [
                            c.description
                            for c in self.__mapper__.columns
                            if c.primary_key
                        ]
                    ]
                )
            }"""
            ")"
        )

    def to_dict(self, keys: list[str] | None = None) -> dict:
        """Return a dictionary representation of the model instance.
        If keys is provided, return only the values of the keys in the list.
        Otherwise, return all the values of the model instance."""

        if keys:
            if any(k not in self.__mapper__.columns for k in keys):
                raise ValueError(
                    "Invalid column provided: {k} not in model columns."
                )
            return {k: getattr(self, k) for k in keys}
        return {
            k.description: getattr(self, k.description)
            for k in self.__mapper__.columns
        }
