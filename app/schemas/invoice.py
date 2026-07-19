from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import List
from datetime import datetime

from app.schemas.denomination import DenominationItem


class InvoiceItemCreate(BaseModel):
    product_id: str
    quantity: int


class InvoiceCreate(BaseModel):
    customer_id: int
    paid_amount: float = 0.0
    denominations: list[DenominationItem] | None = None
    items: List[InvoiceItemCreate]


class InvoiceSummaryResponse(BaseModel):
    id: int
    invoice_number: str
    customer_id: int
    subtotal: float
    total: float
    paid_amount: float
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceItemResponse(BaseModel):
    id: int
    invoice_id: int
    product_code: str
    quantity: int
    price: float
    amount: float
    tax_percentage: float
    tax_amount: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class InvoiceCustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    customer_id: int
    customer: InvoiceCustomerResponse | None = None
    subtotal: float
    tax: float
    total: float
    paid_amount: float
    balance: float
    created_at: datetime
    change_distribution: dict[int, int] | None = None
    items: List[InvoiceItemResponse] = Field(..., alias='invoice_items')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)