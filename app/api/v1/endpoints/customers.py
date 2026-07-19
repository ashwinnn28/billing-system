from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import (get_db,get_current_user)
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.schemas.invoice import InvoiceSummaryResponse
from app.services import CustomerService
from app.services.invoice_service import InvoiceService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    return CustomerService.create_customer(
        db,
        customer
    )


@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return CustomerService.get_customers(db)


@router.get(
    "/{customer_id}/invoices",
    response_model=list[InvoiceSummaryResponse]
)
def get_customer_invoices(
    customer_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return InvoiceService.get_customer_invoices(db, customer_id)