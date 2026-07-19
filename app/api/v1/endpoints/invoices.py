from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import logging

from app.services.pdf_service import PDFService
from app.services.email_service import send_invoice_email
from app.services.invoice_service import InvoiceService

from app.api.deps import (
    get_db,
    get_current_user
)

from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse
)

from app.core.permissions import check_role

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post(
    "/",
    response_model=InvoiceResponse
)
def create_invoice(
    invoice_data: InvoiceCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(check_role(["admin", "staff"]))
):

    try:
        invoice = InvoiceService.create_invoice(db, invoice_data)

        pdf_path = PDFService.generate_invoice_pdf(invoice)

        background_tasks.add_task(
            send_invoice_email,
            invoice.customer.email,
            invoice.id,
            pdf_path,
        )

        return invoice
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to create invoice")


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return InvoiceService.get_invoice(
        db,
        invoice_id
    )