from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import (
    get_db,
    get_current_user
)
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse
)
from app.services import InvoiceService
from app.core.permissions import check_role

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post(
    "/",
    response_model=InvoiceResponse
)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    check_role(
        current_user,
        [
            "admin",
            "staff"
        ]
    )


    return InvoiceService.create_invoice(
        db,
        invoice
    )


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    return InvoiceService.get_invoice(
        db,
        invoice_id
    )