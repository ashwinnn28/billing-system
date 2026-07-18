from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin


class Product(Base, TimestampMixin):
    """
    Product model.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    product_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    available_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    tax_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    invoice_items = relationship(
        "InvoiceItem",
        back_populates="product",
    )