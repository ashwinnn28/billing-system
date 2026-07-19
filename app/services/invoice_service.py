from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from app.models.invoice import Invoice

from app.crud.invoice import create_invoice as create_invoice_crud
from app.crud.invoice import get_invoice_with_items as get_invoice_with_items_crud
from app.crud.invoice import get_invoices_by_customer as get_invoices_by_customer_crud
from app.repositories.invoice_repository import InvoiceRepository
from app.schemas.invoice import InvoiceCreate


class InvoiceService:


    @staticmethod
    def create_invoice(
        db: Session,
        invoice: InvoiceCreate
    ):

        invoice_obj = create_invoice_crud(
            db,
            invoice
        )

        result = get_invoice_with_items_crud(db, invoice_obj.id)
        if hasattr(invoice_obj, 'change_distribution'):
            result.change_distribution = invoice_obj.change_distribution
        return result


    @staticmethod
    def _ensure_email_columns(db: Session):
        try:
            db.rollback()
        except Exception:
            pass

        try:
            db.execute(
                text(
                    """
                    ALTER TABLE invoices
                    ADD COLUMN IF NOT EXISTS email_sent BOOLEAN NOT NULL DEFAULT FALSE
                    """
                )
            )
            db.execute(
                text(
                    """
                    ALTER TABLE invoices
                    ADD COLUMN IF NOT EXISTS email_sent_at TIMESTAMP NULL
                    """
                )
            )
            db.commit()
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_invoice(
        db: Session,
        invoice_id: int
    ):

        try:
            return get_invoice_with_items_crud(db, invoice_id)
        except ProgrammingError as exc:
            try:
                db.rollback()
            except Exception:
                pass
            if "email_sent" in str(exc):
                InvoiceService._ensure_email_columns(db)
                return db.query(Invoice).filter(Invoice.id == invoice_id).first()
            raise

    @staticmethod
    def get_customer_invoices(
        db: Session,
        customer_id: int
    ):
        return get_invoices_by_customer_crud(db, customer_id)

    @staticmethod
    def get_latest_invoice(db: Session):
        try:
            return db.query(Invoice).order_by(Invoice.id.desc()).first()
        except ProgrammingError as exc:
            try:
                db.rollback()
            except Exception:
                pass
            if "email_sent" in str(exc):
                InvoiceService._ensure_email_columns(db)
                return db.query(Invoice).order_by(Invoice.id.desc()).first()
            raise

    @staticmethod
    def mark_email_sent(db: Session, invoice_id: int):
        invoice = InvoiceService.get_invoice(db, invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found for email status update.")

        invoice.email_sent = True
        invoice.email_sent_at = datetime.utcnow()
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice