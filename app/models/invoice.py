from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin
from datetime import datetime


class Invoice(Base, TimestampMixin):
    """
    Invoice model.
    """

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    invoice_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    subtotal: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    tax: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    paid_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    balance: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    email_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    email_sent_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    customer = relationship(
        "Customer",
        back_populates="invoices",
    )

    invoice_items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
    )