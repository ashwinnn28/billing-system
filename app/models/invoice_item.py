from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.database import Base


class InvoiceItem(Base):
    """
    Invoice Item model.
    """

    __tablename__ = "invoice_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id"),
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    tax_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    subtotal: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    invoice = relationship(
        "Invoice",
        back_populates="invoice_items",
    )

    product = relationship(
        "Product",
        back_populates="invoice_items",
    )