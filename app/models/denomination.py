from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class Denomination(Base):
    """
    Shop cash denominations.
    """

    __tablename__ = "denominations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    value: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
    )

    available_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )