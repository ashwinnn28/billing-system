from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.base import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id")
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String(50)
    )

    payment_date = Column(
        DateTime,
        server_default=func.now()
    )