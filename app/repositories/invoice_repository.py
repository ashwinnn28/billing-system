from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate


class InvoiceRepository:


    @staticmethod
    def create(
        db: Session,
        invoice: InvoiceCreate
    ):

        db_invoice = Invoice(
            **invoice.model_dump()
        )

        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)

        return db_invoice


    @staticmethod
    def get_by_id(
        db: Session,
        invoice_id: int
    ):

        return (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )