from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.permissions import check_role
from app.core.roles import UserRole
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)
from app.services.payment_service import PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/",
    response_model=PaymentResponse,
)
def add_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    user=Depends(
        check_role(
            [
                UserRole.ADMIN,
                UserRole.STAFF,
            ]
        )
    ),
):
    return PaymentService.create_payment(
        db,
        payment,
    )


@router.get(
    "/invoice/{invoice_id}",
    response_model=list[PaymentResponse],
)
def get_invoice_payments(
    invoice_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        check_role(
            [
                UserRole.ADMIN,
                UserRole.STAFF,
            ]
        )
    ),
):
    return PaymentService.get_invoice_payments(
        db,
        invoice_id,
    )