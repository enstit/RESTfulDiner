# app/models/_base.py


import re

from sqlalchemy.orm import DeclarativeBase, declared_attr


from app.models import metadata


class BaseModel(DeclarativeBase):
    __abstract__ = True
    metadata = metadata

    # @declared_attr
    # def id(cls) -> Mapped[UUIDType]:
    #     return mapped_column(
    #         cd.ID,
    #         default=lambda: uuid8(domain=cls.__name__),
    #         primary_key=True,
    #         comment=f"Unique {cls.__name__} instance identifier",
    #         sort_order=-1,  # Ensure the id is the first column in the table
    #     )

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

    def to_dict(
        self, keys: list[str] | None = None
    ) -> dict[str, str | int | float]:
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
