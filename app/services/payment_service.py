from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import PaymentCreate


class PaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        payment: PaymentCreate,
    ):

        invoice = (
            db.query(Invoice)
            .filter(
                Invoice.id == payment.invoice_id
            )
            .first()
        )

        if not invoice:
            raise ValueError("Invoice not found")

        if payment.amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero"
            )

        if payment.amount > invoice.balance:
            raise ValueError(
                "Payment exceeds remaining balance"
            )

        invoice.paid_amount += payment.amount

        invoice.balance = (
            invoice.total - invoice.paid_amount
        )

        db_payment = PaymentRepository.create(
            db,
            payment,
            commit=False,
        )

        db.commit()

        db.refresh(invoice)
        db.refresh(db_payment)

        return db_payment

    @staticmethod
    def get_invoice_payments(
        db: Session,
        invoice_id: int,
    ):

        return PaymentRepository.get_by_invoice(
            db,
            invoice_id,
        )