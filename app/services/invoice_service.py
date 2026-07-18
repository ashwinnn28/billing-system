from sqlalchemy.orm import Session

from app.repositories.invoice_repository import InvoiceRepository
from app.schemas.invoice import InvoiceCreate


class InvoiceService:


    @staticmethod
    def create_invoice(
        db: Session,
        invoice: InvoiceCreate
    ):

        return InvoiceRepository.create(
            db,
            invoice
        )


    @staticmethod
    def get_invoice(
        db: Session,
        invoice_id: int
    ):

        return InvoiceRepository.get_by_id(
            db,
            invoice_id
        )