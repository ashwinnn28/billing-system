from sqlalchemy.orm import Session

from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import PaymentCreate


class PaymentService:


    @staticmethod
    def create_payment(
        db: Session,
        payment: PaymentCreate
    ):

        return PaymentRepository.create(
            db,
            payment
        )


    @staticmethod
    def get_invoice_payments(
        db: Session,
        invoice_id: int
    ):

        return PaymentRepository.get_by_invoice(
            db,
            invoice_id
        )