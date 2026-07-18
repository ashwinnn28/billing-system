from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


class PaymentRepository:

    @staticmethod
    def create(
        db: Session,
        payment: PaymentCreate,
        commit: bool = True,
    ):

        db_payment = Payment(
            **payment.model_dump()
        )

        db.add(db_payment)

        if commit:
            db.commit()
            db.refresh(db_payment)

        return db_payment

    @staticmethod
    def get_by_invoice(
        db: Session,
        invoice_id: int,
    ):

        return (
            db.query(Payment)
            .filter(
                Payment.invoice_id == invoice_id
            )
            .all()
        )