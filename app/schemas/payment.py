from datetime import datetime

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    invoice_id: int
    amount: float
    payment_method: str
    reference_number: str | None = None


class PaymentResponse(BaseModel):
    id: int
    invoice_id: int
    amount: float
    payment_method: str
    reference_number: str | None
    payment_date: datetime

    class Config:
        from_attributes = True