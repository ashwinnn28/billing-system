from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.permissions import check_role
from app.api.deps import get_db
from app.core.roles import UserRole
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse
)
from app.services import InvoiceService


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
    db: Session = Depends(get_db)
):

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

@router.post("/")
def add_payment(

    user = Depends(
        check_role(
            [
                UserRole.ADMIN,
                UserRole.STAFF
            ]
        )
    )

):

    return {
        "message":
        "Payment added"
    }